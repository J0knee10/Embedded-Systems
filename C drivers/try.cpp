#include <wiringPi.h>
#include <iostream>

int main() {
    // Initialize WiringPi
    if (wiringPiSetup() == -1) {
        std::cerr << "Failed to initialize WiringPi." << std::endl;
        return 1;
    }

    // Your code logic here

    std::cout << "WiringPi initialized successfully." << std::endl;
    // Example: Blink an LED connected to GPIO pin 0
    pinMode(0, OUTPUT); // Set GPIO pin 0 as output
    for (int i = 0; i < 10; ++i) {
        digitalWrite(0, HIGH); // Turn LED on
        std::cout << "LED is ON" << std::endl;
        delay(500);             // Wait 500 ms
        digitalWrite(0, LOW);  // Turn LED off
        std::cout << "LED is OFF" << std::endl;
        delay(500);             // Wait 500 ms
    }
    return 0;
}