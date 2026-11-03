// Momentum / official Flipper JavaScript example.
// Requires Flipper UART USART and 3.3 V level-crossed wire to ESP32 UART.
// Run from Apps > Scripts after confirming pinout in docs/WIRING.md.
let eventLoop = require("event_loop");
let gui = require("gui");
let submenu = require("gui/submenu");
let serial = require("serial");

serial.setup("usart", 115200);
let menu = submenu.makeWith({items: [
    "Happy", "Surprised", "Listening", "Talking", "Neutral", "Sound", "Speed 42", "Status", "Identify", "Exit"
]});
let commands = ["E:happy\n", "E:surprised\n", "E:listening\n", "E:talking\n",
    "E:neutral\n", "S:1\n", "V:42\n", "Q\n", "I\n"];

eventLoop.subscribe(menu.chosen, function(_sub, index) {
    if (index === 9) {
        eventLoop.stop();
        return;
    }
    serial.write(commands[index]);
    let reply = serial.readln(750);
    print("Mochi: " + (reply === undefined ? "no response" : reply));
});
eventLoop.subscribe(gui.viewDispatcher.navigation, function() { eventLoop.stop(); });
gui.viewDispatcher.switchTo(menu);
eventLoop.run();
serial.end();
