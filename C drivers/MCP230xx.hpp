#ifndef MCP230XX_HPP
#define MCP230XX_HPP

#include <wiringPiI2C.h>
#include <vector>
#include <string>
#include <cstdint>

class MCP230xx {
public:
    MCP230xx(const std::string& chip, int i2cAddr);

    int readRegister(uint8_t reg);
    void writeRegister(uint8_t reg, uint8_t value);

    void setMode(int pin, const std::string& mode, const std::string& pullUp = "disable");
    void output(int pin, int value);
    int input(int pin);
    int inputAtInterrupt(int pin);
    void invertInput(int pin, bool invert = false);
    void interruptOptions(const std::string& outputType = "activehigh", const std::string& bankControl = "separate");
    void setRegisterAddressing(const std::string& regScheme = "8bit");

    void registerReset();

private:
    std::pair<uint8_t, int> selectRegisterBit(int pin, uint8_t reg8A, uint8_t reg16A, uint8_t reg8B, uint8_t reg16B);

    std::string chip;
    std::string bank;
    int fd;
    int i2cAddress;
};

#endif
