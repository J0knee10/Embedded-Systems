#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <arpa/inet.h>

#define PORT 8080

sem_t thread_limit;

void* handle_client(void* socket_desc) {
    int new_socket = *(int*)socket_desc;
    int number, result;

    // Receive number
    if (recv(new_socket, &number, sizeof(number), 0) > 0) {
        printf("Thread [%lu]: Received %d. Calculating...\n", pthread_self(), number);
        
        // Functionality: multiply by 5
        result = number * 5;
        
        // Send back
        send(new_socket, &result, sizeof(result), 0);
    }

    printf("Thread [%lu]: Finished. Closing connection.\n", pthread_self());
    close(new_socket);
    free(socket_desc);

    // Release semaphore slot
    sem_post(&thread_limit);
    return NULL;
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // Initialize semaphore with value 3
    sem_init(&thread_limit, 0, 3);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", PORT);

    while (1) {
        // Wait for an available thread slot
        sem_wait(&thread_limit);

        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            sem_post(&thread_limit);
            continue;
        }

        pthread_t thread_id;
        int *new_sock = malloc(sizeof(int));
        *new_sock = new_socket;

        if (pthread_create(&thread_id, NULL, handle_client, (void*)new_sock) < 0) {
            perror("Could not create thread");
            free(new_sock);
            sem_post(&thread_limit);
        }

        pthread_detach(thread_id); // Auto-reclaim resources upon completion
    }

    sem_destroy(&thread_limit);
    return 0;
}