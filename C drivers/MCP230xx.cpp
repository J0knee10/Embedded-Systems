#include "MCP230xx.hpp"
#include <iostream>

MCP230xx::MCP230xx(const std::string& chip, int i2cAddr) : chip(chip), i2cAddress(i2cAddr) {
    fd = wiringPiI2CSetup(i2cAddress);
    if (fd == -1) {
        std::cerr << "Failed to init I2C device at address 0x" << std::hex << i2cAddress << std::endl;
    }
    bank = (chip == "MCP23017") ? "16bit" : "8bit";
}

int MCP230xx::readRegister(uint8_t reg) {
    return wiringPiI2CReadReg8(fd, reg);
}

void MCP230xx::writeRegister(uint8_t reg, uint8_t value) {
    wiringPiI2CWriteReg8(fd, reg, value);
}

std::pair<uint8_t, int> MCP230xx::selectRegisterBit(int pin, uint8_t reg8A, uint8_t reg16A, uint8_t reg8B, uint8_t reg16B) {
    int bit = (pin < 8) ? pin : pin - 8;
    uint8_t reg = 0;

    if (pin < 8) {
        reg = (bank == "16bit") ? reg16A : reg8A;
    } else {
        reg = (bank == "16bit") ? reg16B : reg8B;
    }
    return {reg, bit};
}

void MCP230xx::setMode(int pin, const std::string& mode, const std::string& pullUp) {
    auto [reg, bit] = selectRegisterBit(pin, 0x00, 0x00, 0x10, 0x01);  // IODIRA/B
    uint8_t regVal = readRegister(reg);

    if (mode == "output") {
        regVal &= ~(1 << bit);
    } else {
        regVal |= (1 << bit);
    }
    writeRegister(reg, regVal);

    if (mode == "input") {
        auto [pullReg, pullBit] = selectRegisterBit(pin, 0x06, 0x0C, 0x16, 0x0D);  // GPPU
        regVal = readRegister(pullReg);
        if (pullUp == "enable") {
            regVal |= (1 << pullBit);
        } else {
            regVal &= ~(1 << pullBit);
        }
        writeRegister(pullReg, regVal);
    }
}

void MCP230xx::output(int pin, int value) {
    auto [reg, bit] = selectRegisterBit(pin, 0x09, 0x14, 0x1A, 0x15); // OLAT
    uint8_t regVal = readRegister(reg);

    if (value == 1) {
        regVal |= (1 << bit);
    } else {
        regVal &= ~(1 << bit);
    }
    writeRegister(reg, regVal);
}

int MCP230xx::input(int pin) {
    auto [reg, bit] = selectRegisterBit(pin, 0x09, 0x12, 0x19, 0x13);  // GPIO
    uint8_t regVal = readRegister(reg);
    return (regVal >> bit) & 0x1;
}

int MCP230xx::inputAtInterrupt(int pin) {
    auto [reg, bit] = selectRegisterBit(pin, 0x08, 0x10, 0x18, 0x11); // INTCAP
    uint8_t regVal = readRegister(reg);
    return (regVal >> bit) & 0x1;
}

void MCP230xx::invertInput(int pin, bool invert) {
    auto [reg, bit] = selectRegisterBit(pin, 0x01, 0x02, 0x11, 0x03); // IPOL
    uint8_t regVal = readRegister(reg);

    if (invert) {
        regVal |= (1 << bit);
    } else {
        regVal &= ~(1 << bit);
    }
    writeRegister(reg, regVal);
}

void MCP230xx::interruptOptions(const std::string& outputType, const std::string& bankControl) {
    uint8_t reg = (bank == "16bit") ? 0x0A : 0x05; // IOCON
    uint8_t val = readRegister(reg) & 0b10111001;

    uint8_t mirrorBit = (bankControl == "both") ? 1 : 0;
    uint8_t odrBit = 0;
    uint8_t intpolBit = 0;

    if (outputType == "opendrain") {
        odrBit = 1;
    } else if (outputType == "activehigh") {
        intpolBit = 1;
    }

    val |= (mirrorBit << 6) | (odrBit << 2) | (intpolBit << 1);
    writeRegister(reg, val);
}

void MCP230xx::setRegisterAddressing(const std::string& regScheme) {
    uint8_t reg = (bank == "16bit") ? 0x0A : 0x05; // IOCON
    uint8_t regVal = readRegister(reg) & 0b01111111;

    if (regScheme == "16bit") {
        bank = "16bit";
    } else {
        regVal |= (1 << 7);
        bank = "8bit";
    }
    writeRegister(reg, regVal);
}

void MCP230xx::registerReset() {
    if (chip == "MCP23008") {
        writeRegister(0x00, 0xFF);  // IODIR
        for (int i = 1; i < 12; ++i) {
            writeRegister(i, 0x00);
        }
    } else {
        setRegisterAddressing("16bit");
        writeRegister(0x00, 0xFF);
        writeRegister(0x01, 0xFF);
        for (int i = 2; i < 22; ++i) {
            writeRegister(i, 0x00);
        }
    }
}
