#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <time.h>

#define PORT 8080
#define SERVER_IP "127.0.0.1" // Change to your RPi IP address

void start_client(int id) {
    int sock = 0;
    struct sockaddr_in serv_addr;
    int number, response;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return;
    }

    // Generate random number
    srand(time(NULL) ^ (getpid() << 16));
    number = rand() % 100;

    printf("Client [%d]: Sending number %d to server...\n", id, number);
    send(sock, &number, sizeof(number), 0);
    
    read(sock, &response, sizeof(response));
    printf("Client [%d]: Received from server: %d\n", id, response);

    close(sock);
}

int main() {
    for (int i = 0; i < 3; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            // Child process
            start_client(i + 1);
            exit(0);
        } else if (pid < 0) {
            perror("Fork failed");
        }
    }

    // Parent waits for all children to finish
    for (int i = 0; i < 3; i++) {
        wait(NULL);
    }

    return 0;
}