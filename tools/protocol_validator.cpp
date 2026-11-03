// Standalone hardware-independent validation of the same parser firmware uses.
// g++ -std=c++11 -Ifirmware/include tools/protocol_validator.cpp -o /tmp/mochi-validator
#include "mochi_protocol.h"
#include <stdio.h>
#include <string.h>
int main(int argc, char** argv) {
    if (argc != 2) return 64;
    bool valid = mochi::validCommand(argv[1], strlen(argv[1]));
    puts(valid ? "VALID" : "INVALID");
    return valid ? 0 : 2;
}
