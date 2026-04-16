#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <linux/gpio.h>
#include <stdlib.h>
#include <time.h>

// Pins
#define G_LED 4
#define Y_LED 17
#define R_LED 27
#define BUZZ  18
#define BTN   11

void set_outputs(int fd, int g, int y, int r, int b) {
    struct gpiohandle_data data = {{g, y, r, b}};
    ioctl(fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);
}

// Function to generate a tone for a specific duration (milliseconds)
void play_buzzer(int fd, int duration_ms) {
    int cycles = duration_ms; // Simplified: toggle every 1ms for ~500Hz
    for (int i = 0; i < cycles/2; i++) {
        struct gpiohandle_data on = {{0, 0, 1, 1}}; // Red ON, Buzz ON
        struct gpiohandle_data off = {{0, 0, 1, 0}}; // Red ON, Buzz OFF
        ioctl(fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &on);
        usleep(1000); // 1ms high
        ioctl(fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &off);
        usleep(1000); // 1ms low
    }
}

int main() {
    int fd0 = open("/dev/gpiochip0", O_RDWR);
    srand(time(NULL));

    struct gpiohandle_request out_req = {.lines = 4, .lineoffsets = {G_LED, Y_LED, R_LED, BUZZ}, .flags = GPIOHANDLE_REQUEST_OUTPUT};
    ioctl(fd0, GPIO_GET_LINEHANDLE_IOCTL, &out_req);

    struct gpiohandle_request btn_req = {.lines = 1, .lineoffsets = {BTN}, .flags = GPIOHANDLE_REQUEST_INPUT};
    ioctl(fd0, GPIO_GET_LINEHANDLE_IOCTL, &btn_req);

    int state = 0; // 0:G, 1:Y, 2:R
    while(1) {
        if (state == 0) { // GREEN
            set_outputs(out_req.fd, 1, 0, 0, 0);
            sleep(2);
            state = 1;
        } 
        else if (state == 1) { // YELLOW
            set_outputs(out_req.fd, 0, 1, 0, 0);
            int timeout = (rand() % 8) + 3;
            int pressed = 0;
            for (int i = 0; i < timeout * 50; i++) { // Check every 20ms
                struct gpiohandle_data b_data;
                ioctl(btn_req.fd, GPIOHANDLE_GET_LINE_VALUES_IOCTL, &b_data);
                if (b_data.values[0]) { pressed = 1; break; }
                usleep(20000);
            }
            state = pressed ? 2 : 0;
        } 
        else if (state == 2) { // RED + BUZZ
            // Instead of sleep(2), we call our play_buzzer for 2000ms
            play_buzzer(out_req.fd, 2000);
            state = 0;
        }
    }
    return 0;
}
