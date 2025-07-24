
// ADC_driver.cpp
// This code reads data from four ADS1115 ADCs connected to a Raspberry Pi via I2C.
// needed libraries:
// - Adafruit_ADS1X15_RPi: Library for ADS1115/ADS1015 ADCs https://github.com/hallgrimur1471/Adafruit_ADS1X15_RPi.git
// - wiringPi: Library for GPIO and I2C communication on Raspberry Pi https://github.com/WiringPi/WiringPi.git
// run this in CLI: g++ -std=c++11 -W -o ADC_driver ADC_driver.cpp Adafruit_ADS1X15_RPi/Adafruit_ADS1015.cpp -lwiringPi


#include "Adafruit_ADS1X15_RPi/Adafruit_ADS1015.h"
#include <iostream>
#include <chrono>
#include <thread>
#include <iomanip>
#include <vector>

// Create ADS1115 instances at each I2C address
Adafruit_ADS1115 ads1(0x48);
Adafruit_ADS1115 ads2(0x49);
Adafruit_ADS1115 ads3(0x4A);
Adafruit_ADS1115 ads4(0x4B);

// ADS1115 has 16-bit resolution with gain of ±4.096V => 1 LSB = 125µV
const float LSB_SIZE = 0.000125f;

// Function to read voltage from a channel
float readADC(Adafruit_ADS1115 &adc, uint8_t channel) {
    int16_t result = adc.readADC_SingleEnded(channel);
    return result * LSB_SIZE;  // Convert to volts manually
}

int main() {
    // Initialize ADS1115s
    ads1.begin();
    ads2.begin();
    ads3.begin();
    ads4.begin();

    // Set gain (±4.096V)
    ads1.setGain(GAIN_ONE);
    ads2.setGain(GAIN_ONE);
    ads3.setGain(GAIN_ONE);
    ads4.setGain(GAIN_ONE);

    std::cout << "ADS1115 initialized (Gain ±4.096V)" << std::endl;

    auto start = std::chrono::steady_clock::now();
    auto cycle_start = std::chrono::steady_clock::now();

    while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::steady_clock::now() - start).count() < 3) {
        std::vector<float> data(16, 0.0f);

        for (int i = 0; i < 4; ++i) {
            data[i]      = readADC(ads1, i);
            data[i + 4]  = readADC(ads2, i);
            data[i + 8]  = readADC(ads3, i);
            data[i + 12] = readADC(ads4, i);
        }

        std::cout << "Data: ";
        for (const auto &val : data) {
            std::cout << std::fixed << std::setprecision(3) << val << "V ";
        }

        auto cycle_end = std::chrono::steady_clock::now();
        std::cout << "Cycle Time: "
                  << std::chrono::duration_cast<std::chrono::milliseconds>(cycle_end - cycle_start).count()
                  << " ms" << std::endl;

        cycle_start = std::chrono::steady_clock::now();
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }

    std::cout << "ADC read complete." << std::endl;
    return 0;
}