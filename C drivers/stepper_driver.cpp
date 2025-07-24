#include <iostream>
#include <string>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <cstring>
#include "MCP230xx.hpp"

class Stepper {
private:
    int ID;
    int pin_EN, pin_MS1, pin_MS2, pin_DIR;
    int microstep;
    int SPR;
    int RPM;
    int status;
    MCP230xx* mcp;
    int uart_fd;
    std::string uart_addr;

public:
    Stepper(int id, MCP* mcp_obj) : ID(id), SPR(200), RPM(0), status(1), mcp(mcp_obj), uart_addr("/dev/ttyS0") {
        init_uart();
        std::cout << "Stepper_driver: finished init. stepper" << ID << std::endl;
    }

    void config(int en, int ms1, int ms2, int dir, int microstep_val) {
        pin_EN = en; pin_MS1 = ms1; pin_MS2 = ms2; pin_DIR = dir;
        microstep = microstep_val;

        mcp->setMode(pin_EN, "output");
        mcp->setMode(pin_MS1, "output");
        mcp->setMode(pin_MS2, "output");
        mcp->setMode(pin_DIR, "output");

        mcp->digitalWrite(pin_EN, 1);

        if (microstep == 8) {
            mcp->digitalWrite(pin_MS2, 0);
            mcp->digitalWrite(pin_MS1, 0);
        } else if (microstep == 16) {
            mcp->digitalWrite(pin_MS2, 1);
            mcp->digitalWrite(pin_MS1, 1);
        } else if (microstep == 32) {
            mcp->digitalWrite(pin_MS2, 0);
            mcp->digitalWrite(pin_MS1, 1);
        } else if (microstep == 64) {
            mcp->digitalWrite(pin_MS2, 1);
            mcp->digitalWrite(pin_MS1, 0);
        }
    }

    void init_uart() {
        uart_fd = open(uart_addr.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
        if (uart_fd == -1) {
            std::cerr << "Failed to open UART." << std::endl;
            return;
        }

        struct termios options;
        tcgetattr(uart_fd, &options);
        options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
        options.c_iflag = IGNPAR;
        options.c_oflag = 0;
        options.c_lflag = 0;
        tcflush(uart_fd, TCIFLUSH);
        tcsetattr(uart_fd, TCSANOW, &options);

        std::string start_cmd = "start," + std::to_string(ID) + ",\n";
        char buffer[256];
        memset(buffer, 0, sizeof(buffer));

        for (int i = 0; i < 20; ++i) {
            write(uart_fd, start_cmd.c_str(), start_cmd.length());
            usleep(100000);  // 100 ms
            int n = read(uart_fd, buffer, sizeof(buffer) - 1);
            buffer[n] = '\0';

            std::string reply(buffer);
            if (reply.find("started," + std::to_string(ID)) == 0) {
                std::cout << "stepper_driver: UART handshake OK for stepper" << ID << std::endl;
                return;
            }
        }
        std::cerr << "stepper_driver: UART timeout on stepper" << ID << std::endl;
    }

    void set_RPM(int rpm) {
        RPM = rpm;
        int freq = 10;
        int duty = 0;

        if (rpm == 0) {
            mcp->digitalWrite(pin_EN, 1);
            mcp->digitalWrite(pin_DIR, 1);
        } else {
            mcp->digitalWrite(pin_EN, 0);
            freq = std::abs(rpm * SPR * microstep / 60);
            duty = 30000;
            mcp->digitalWrite(pin_DIR, (rpm > 0) ? 1 : 0);
        }

        std::string cmd = "set," + std::to_string(ID) + "," +
                          std::to_string(freq) + "," +
                          std::to_string(duty) + "," +
                          std::to_string(rpm) + "\n";

        write(uart_fd, cmd.c_str(), cmd.length());
    }

    void off() {
        mcp->digitalWrite(pin_EN, 1);
    }
};
