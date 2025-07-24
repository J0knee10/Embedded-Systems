#include "MCP230xx.hpp"
#include <unistd.h>

int main() {
    MCP230xx mcp1("MCP23017", 0x27);
    MCP230xx mcp2("MCP23008", 0x21);
    MCP230xx mcp3("MCP23008", 0x24);

    mcp1.setMode(0, "output");
    while (true) {
        mcp1.output(0, 1);
        sleep(1);
        mcp1.output(0, 0);
        sleep(1);
    }
}
