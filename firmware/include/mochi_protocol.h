#pragma once
// MOCHI/1 reference parser shared with host-side conformance tests.
// C++11, no dynamic allocation, Arduino dependencies or heap allocations.
#include <stddef.h>
#include <string.h>

namespace mochi {

static inline bool validSpeed(const char* s, size_t n) {
    if (!n) return false;
    bool dot = false, hasDigit = false, fractionalNonzero = false;
    unsigned int whole = 0;
    for (size_t i = 0; i < n; ++i) {
        const char ch = s[i];
        if (ch == '.') {
            if (dot) return false;
            dot = true;
        } else if (ch >= '0' && ch <= '9') {
            hasDigit = true;
            if (!dot) {
                whole = whole * 10u + (unsigned int)(ch - '0');
                // Limit during parsing so large inputs cannot overflow.
                if (whole > 250u) return false;
            } else if (ch != '0') {
                fractionalNonzero = true;
            }
        } else return false;
    }
    return hasDigit && whole <= 250u && !(whole == 250u && fractionalNonzero);
}

static inline bool equals(const char* s, size_t n, const char* literal) {
    return strlen(literal) == n && memcmp(s, literal, n) == 0;
}

static inline bool validCommand(const char* s, size_t n) {
    if (!s || n < 1 || n > 20) return false;
    for (size_t i = 0; i < n; ++i) if ((unsigned char)s[i] < 32 || (unsigned char)s[i] > 126) return false;
    if (equals(s, n, "Q") || equals(s, n, "I")) return true;
    if (equals(s, n, "P:0") || equals(s, n, "P:1") ||
        equals(s, n, "S:1") || equals(s, n, "S:2") || equals(s, n, "S:3")) return true;
    if (n < 3 || s[1] != ':') return false;
    if (s[0] == 'V') return validSpeed(s + 2, n - 2);
    if (s[0] == 'E') {
        const char* name = s + 2;
        const size_t length = n - 2;
        const char* const faces[] = {"neutral", "happy", "surprised", "sleepy", "listening", "talking", "sad"};
        for (size_t i = 0; i < sizeof(faces)/sizeof(faces[0]); ++i)
            if (equals(name, length, faces[i])) return true;
    }
    return false;
}

} // namespace mochi
