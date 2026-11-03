#pragma once
// Reference pinout for generic ESP32-S3 DevKitC-1 ONLY; verify your board.
// Set these to 0 for USB/UART/BLE-only proof of concept without peripherals.
#define MOCHI_USE_ST7789 1
#define MOCHI_USE_I2S_SPEAKER 1

#define MOCHI_TFT_SCLK 12
#define MOCHI_TFT_MOSI 11
#define MOCHI_TFT_CS 10
#define MOCHI_TFT_DC 9
#define MOCHI_TFT_RST 14

#define MOCHI_I2S_BCLK 4
#define MOCHI_I2S_LRCK 5
#define MOCHI_I2S_DOUT 6

#define MOCHI_UART_RX 17
#define MOCHI_UART_TX 18
#define MOCHI_UART_BAUD 115200

// These UUIDs identify a prototype control service, NOT an audio profile.
#define MOCHI_SERVICE_UUID "8ef6c3e0-6d43-4a81-891e-e9e380720001"
#define MOCHI_WRITE_UUID   "8ef6c3e0-6d43-4a81-891e-e9e380720002"
#define MOCHI_NOTIFY_UUID  "8ef6c3e0-6d43-4a81-891e-e9e380720003"
