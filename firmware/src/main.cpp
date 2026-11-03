#include "mochi_protocol.h"
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLE2902.h>
#include <BLEServer.h>
#include <SPI.h>
#include <math.h>
#include <string>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
#include "config.h"

#if MOCHI_USE_ST7789
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
Adafruit_ST7789 display(&SPI, MOCHI_TFT_CS, MOCHI_TFT_DC, MOCHI_TFT_RST);
#endif
#if MOCHI_USE_I2S_SPEAKER
#include <driver/i2s.h>
#endif

// MOCHI/1 uses single small ASCII messages (<=20 bytes), avoiding BLE fragmentation.
// Accepted commands: E:happy|neutral|surprised|sleepy|listening|talking|sad
// V:<0..250> (speed km/h); S:1..3 (short tone); P:0|1; Q (status); I (identity)
// Each UART line ends in '\n'. Each BLE write contains one complete command.
// Do not use for sensitive data: BLE authentication is NOT implemented in r0.

struct CommandPacket { char bytes[24]; uint8_t origin; }; // origin: 1 BLE, 2 UART, 3 USB
QueueHandle_t commandQueue;
BLECharacteristic* eventCharacteristic = nullptr;
BLEAdvertising* advertising = nullptr;
volatile bool restartAdvertising = false;
HardwareSerial linkUart(1);
String uartBuffer, usbBuffer;
bool uartOverflow = false, usbOverflow = false;

struct MochiState {
  String expression = "neutral";
  float speedKmh = 0.0f;
  bool ptt = false;
  uint32_t updated = 0;
} state;

class ServerCallbacks : public BLEServerCallbacks {
  void onDisconnect(BLEServer*) override { restartAdvertising = true; }
};

static void queueCommand(const char* text, size_t length, uint8_t origin) {
  if (!text || !length || length > 20 || !commandQueue) return;
  CommandPacket pkt{};
  memcpy(pkt.bytes, text, length);
  pkt.bytes[length] = '\0';
  pkt.origin = origin;
  xQueueSend(commandQueue, &pkt, 0);  // Never draw/I2S-block in BLE callback.
}

class WriteCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* characteristic) override {
    std::string val = characteristic->getValue();
    queueCommand(val.data(), val.size(), 1);
  }
};

static bool faceAllowed(const String& expr) {
  return expr == "neutral" || expr == "happy" || expr == "surprised" ||
         expr == "sleepy" || expr == "listening" || expr == "talking" ||
         expr == "sad";
}

static void renderFace() {
#if MOCHI_USE_ST7789
  display.fillScreen(ST77XX_BLACK);
  const uint16_t colour = ST77XX_CYAN;
  const int left = 75, right = 165;
  bool closed = (state.expression == "sleepy");
  bool surprised = (state.expression == "surprised");
  if (closed) {
    display.drawFastHLine(left - 22, 104, 44, colour);
    display.drawFastHLine(right - 22, 104, 44, colour);
  } else if (surprised) {
    display.fillCircle(left, 96, 22, colour);
    display.fillCircle(right, 96, 22, colour);
    display.fillCircle(left, 96, 11, ST77XX_BLACK);
    display.fillCircle(right, 96, 11, ST77XX_BLACK);
  } else {
    display.fillRoundRect(left - 25, 75, 48, 48, 16, colour);
    display.fillRoundRect(right - 25, 75, 48, 48, 16, colour);
  }
  if (surprised || state.expression == "talking") {
    display.fillCircle(120, 160, surprised ? 18 : 12, colour);
    display.fillCircle(120, 160, surprised ? 10 : 6, ST77XX_BLACK);
  } else if (state.expression == "happy") {
    display.drawRoundRect(88, 137, 64, 32, 18, colour);
    display.fillRect(86, 135, 68, 18, ST77XX_BLACK);
  } else if (state.expression == "sad") {
    display.drawRoundRect(91, 157, 58, 25, 12, colour);
    display.fillRect(89, 170, 62, 14, ST77XX_BLACK);
  } else {
    display.drawFastHLine(103, 160, 34, colour);
  }
  display.setTextColor(ST77XX_WHITE);
  display.setTextSize(1);
  display.setCursor(8, 8); display.print("OPEN MOCHI r0");
  display.setCursor(8, 223);
  display.print(state.speedKmh, 1); display.print(" km/h");
  if (state.ptt) { display.setCursor(188, 223); display.print("PTT"); }
#endif
}

static void playTone(uint8_t id) {
#if MOCHI_USE_I2S_SPEAKER
  // Small, deterministic sound effects only: NOT speech or a Bluetooth audio profile.
  const int freq = id == 1 ? 620 : (id == 2 ? 880 : 420);
  const int durationMs = id == 3 ? 240 : 120;
  const int rate = 16000;
  int16_t chunk[128 * 2]; // duplicate into L/R channels
  const int totalFrames = rate * durationMs / 1000;
  for (int pos = 0; pos < totalFrames; pos += 128) {
    int frames = min(128, totalFrames - pos);
    for (int j = 0; j < frames; ++j) {
      const int index = pos + j;
      float envelope = sinf(3.14159265f * float(index) / float(totalFrames));
      int16_t sample = static_cast<int16_t>(3200 * envelope * sinf(2 * 3.14159265f * freq * index / rate));
      chunk[2 * j] = sample; chunk[2 * j + 1] = sample;
    }
    size_t written = 0;
    i2s_write(I2S_NUM_0, chunk, frames * 2 * sizeof(int16_t), &written, portMAX_DELAY);
  }
#else
  Serial.printf("[sound] simulated tone %u\n", id);
#endif
}

static void outputResponse(const String& result, uint8_t origin) {
  Serial.println(result);
  if (origin == 2) linkUart.println(result);
  if (eventCharacteristic) {
    eventCharacteristic->setValue(std::string(result.c_str())); // Arduino ESP32 2.0.17 API
    eventCharacteristic->notify(); // Subscriber optional; libraries handle no subscribers.
  }
}

static void handleCommand(const String& raw, uint8_t origin) {
  const String& cmd = raw;
  if (!mochi::validCommand(cmd.c_str(), cmd.length())) {
    outputResponse("ERR:BAD_COMMAND", origin);
    return;
  }
  String answer = "ERR:BAD_COMMAND";
  bool redraw = false;
  if (cmd == "Q") {
    answer = "ST:" + state.expression + "," + String(state.speedKmh, 1);
  } else if (cmd == "I") {
    answer = "ID:0.2,esp32s3";
  } else if (cmd.startsWith("E:")) {
    String expression = cmd.substring(2);
    if (faceAllowed(expression)) {
      state.expression = expression; redraw = true; answer = "OK:E:" + expression;
    } else answer = "ERR:FACE";
  } else if (cmd.startsWith("V:")) {
    String n = cmd.substring(2);
    float speed = strtof(n.c_str(), nullptr);
    // Complete numeric syntax and range already validated before strtof.
    state.speedKmh = speed; redraw = true; answer = "OK:V";
  } else if (cmd == "S:1" || cmd == "S:2" || cmd == "S:3") {
    answer = "OK:S";
    playTone(cmd.charAt(2) - '0');
  } else if (cmd == "P:0" || cmd == "P:1") {
    state.ptt = (cmd == "P:1"); redraw = true; answer = "OK:P";
  }
  state.updated = millis();
  if (redraw) renderFace();
  outputResponse(answer, origin);
}

static void processLine(Stream& port, String& buffer, bool& overflow, uint8_t origin) {
  while (port.available()) {
    int byte = port.read();
    if (byte < 0) break;
    if (byte == '\r') continue;
    if (byte == '\n') {
      if (!overflow && buffer.length()) queueCommand(buffer.c_str(), buffer.length(), origin);
      buffer = ""; overflow = false;
    } else if (!overflow && byte >= 32 && byte <= 126) {
      if (buffer.length() < 20) buffer += char(byte);
      else { buffer = ""; overflow = true; } // reject whole oversized line
    } else if (byte < 32 || byte > 126) {
      buffer = ""; overflow = true;
    }
  }
}

void setup() {
  Serial.begin(115200);
  linkUart.begin(MOCHI_UART_BAUD, SERIAL_8N1, MOCHI_UART_RX, MOCHI_UART_TX);
  commandQueue = xQueueCreate(12, sizeof(CommandPacket));
#if MOCHI_USE_ST7789
  SPI.begin(MOCHI_TFT_SCLK, -1, MOCHI_TFT_MOSI, MOCHI_TFT_CS);
  display.init(240, 240);
  display.setRotation(0);
#endif
#if MOCHI_USE_I2S_SPEAKER
  i2s_config_t audio{};
  audio.mode = static_cast<i2s_mode_t>(I2S_MODE_MASTER | I2S_MODE_TX);
  audio.sample_rate = 16000;
  audio.bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT;
  audio.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
  audio.communication_format = I2S_COMM_FORMAT_STAND_I2S;
  audio.dma_buf_count = 4; audio.dma_buf_len = 128;
  audio.tx_desc_auto_clear = true;
  i2s_driver_install(I2S_NUM_0, &audio, 0, nullptr);
  i2s_pin_config_t pin{};
  pin.bck_io_num = MOCHI_I2S_BCLK;
  pin.ws_io_num = MOCHI_I2S_LRCK;
  pin.data_out_num = MOCHI_I2S_DOUT;
  pin.data_in_num = I2S_PIN_NO_CHANGE;
  i2s_set_pin(I2S_NUM_0, &pin);
  i2s_zero_dma_buffer(I2S_NUM_0);
#endif
  renderFace();
  BLEDevice::init("OpenMochi-r0");
  BLEServer* server = BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());
  BLEService* service = server->createService(MOCHI_SERVICE_UUID);
  BLECharacteristic* input = service->createCharacteristic(MOCHI_WRITE_UUID, BLECharacteristic::PROPERTY_WRITE);
  input->setCallbacks(new WriteCallbacks());
  eventCharacteristic = service->createCharacteristic(MOCHI_NOTIFY_UUID,
                          BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);
  eventCharacteristic->addDescriptor(new BLE2902());
  eventCharacteristic->setValue("ST:neutral,0");
  service->start();
  advertising = BLEDevice::getAdvertising();
  advertising->addServiceUUID(MOCHI_SERVICE_UUID);
  advertising->setScanResponse(true);
  advertising->start();
  Serial.println("OpenMochi r0.2 ready. UART/USB accepts E:happy, V:42, S:1, P:1, Q");
}

void loop() {
  processLine(linkUart, uartBuffer, uartOverflow, 2);
  processLine(Serial, usbBuffer, usbOverflow, 3);
  CommandPacket pkt{};
  while (xQueueReceive(commandQueue, &pkt, 0) == pdTRUE) handleCommand(String(pkt.bytes), pkt.origin);
  if (restartAdvertising) {
    restartAdvertising = false;
    delay(150);
    advertising->start();
  }
  delay(5);
}
