#include <iostream>
#include <thread>
#include <chrono>
#include "MCP230xx.hpp" // Using provided MCP driver

class Valve {
private:
    MCP& mcp;
    int status[8];
    int mcp_channel_index[8];

public:
    Valve(MCP& mcp_driver) : mcp(mcp_driver) {
        for (int i = 0; i < 8; ++i) {
            status[i] = 0;
            mcp_channel_index[i] = -1;
        }
    }

    void setChannelMap(const int map[8]) {
        for (int i = 0; i < 8; ++i) {
            mcp_channel_index[i] = map[i];
        }
    }

    void actuate(const int level[8]) {
        for (int i = 0; i < 8; ++i) {
            if (level[i] >= 0) {
                mcp.output(mcp_channel_index[i], level[i]);
                status[i] = level[i];
            }
        }
    }

    void all_on() {
        for (int i = 0; i < 8; ++i) {
            mcp.output(mcp_channel_index[i], 1);
            status[i] = 1;
        }
    }

    void all_off() {
        for (int i = 0; i < 8; ++i) {
            mcp.output(mcp_channel_index[i], 0);
            status[i] = 0;
        }
    }
};

int main() {
    int address1 = 0x27; // MCP23017
    int address2 = 0x21; // MCP23008
    int address3 = 0x24; // MCP23008 (stepper)

    // MCP mcp1("MCP23017", address1);
    // MCP mcp2("MCP23008", address2);
    MCP mcp3("MCP23008", address3);

    // Output tests
    // std::cout << "start output test" << std::endl;
    // for (int i = 0; i < 16; ++i) mcp1.set_mode(i, "output");
    // for (int i = 0; i < 8; ++i) mcp2.set_mode(i, "output");

    for (int i = 0; i < 8; ++i) mcp3.set_mode(i, "output");

    // Uncomment to test MCP1 outputs
    /*
    mcp1.output(0, 1);
    mcp1.output(1, 1);
    mcp1.output(2, 1);
    mcp1.output(3, 1);
    mcp1.output(4, 0);
    mcp1.output(5, 0);
    mcp1.output(6, 0);
    mcp1.output(7, 0);
    mcp1.output(8, 0);
    mcp1.output(9, 0);
    mcp1.output(10, 1);
    mcp1.output(11, 1);
    mcp1.output(12, 1);
    mcp1.output(13, 1);
    mcp1.output(14, 1);
    mcp1.output(15, 1);
    */

    // Uncomment to test MCP2 outputs
    /*
    mcp2.output(0, 1);
    mcp2.output(1, 1);
    mcp2.output(2, 0);
    mcp2.output(3, 0);
    mcp2.output(4, 0);
    mcp2.output(5, 0);
    mcp2.output(6, 1);
    mcp2.output(7, 1);
    */

    // Set MCP3 outputs to low
    for (int i = 0; i < 8; ++i) mcp3.output(i, 0);
    std::cout << "MCP3 initialized" << std::endl;

    Valve valve(mcp3);
    int valve_map[8] = {0, 1, 2, 3, 4, 5, 6, 7};
    valve.setChannelMap(valve_map);

    valve.all_on();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    valve.all_off();
    std::this_thread::sleep_for(std::chrono::seconds(2));

    return 0;
}
