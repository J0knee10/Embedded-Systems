#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFFER_SIZE 4

// Shared Global State
int circ_buffer[BUFFER_SIZE] = {0};
int write_idx = 0;
int total_sum = 0;
pthread_mutex_t lock; // The "Key" to the critical section

// Structure for the response to the client
struct server_reply {
    int slot_index;
    int current_sum;
};

void* handle_client(void* arg) {
    int sock = *(int*)arg;
    int received_val;
    struct server_reply reply;

    if (read(sock, &received_val, sizeof(int)) > 0) {
        
        // --- START CRITICAL SECTION ---
        pthread_mutex_lock(&lock);
        
        reply.slot_index = write_idx;
        circ_buffer[write_idx] = received_val;
        total_sum += received_val;
        
        printf("[Server] Received: %d | Slot: %d | Total Sum: %d\n", 
                received_val, reply.slot_index, total_sum);

        // Update index for next thread (circular logic)
        write_idx = (write_idx + 1) % BUFFER_SIZE;
        reply.current_sum = total_sum;

        pthread_mutex_unlock(&lock);
        // --- END CRITICAL SECTION ---

        write(sock, &reply, sizeof(struct server_reply));
    }

    close(sock);
    free(arg);
    return NULL;
}

int main(int argc, char *argv[]) {
    int sockfd, newsockfd, port;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t clilen = sizeof(cli_addr);

    if (argc < 2) { printf("Usage: %s [port]\n", argv[0]); exit(1); }

    pthread_mutex_init(&lock, NULL);
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(atoi(argv[1]));

    bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    listen(sockfd, 10);

    printf("PC Server listening on port %s...\n", argv[1]);

    while (1) {
        newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr, &clilen);
        pthread_t tid;
        int *new_sock = malloc(sizeof(int));
        *new_sock = newsockfd;
        pthread_create(&tid, NULL, handle_client, new_sock);
        pthread_detach(tid);
    }

    pthread_mutex_destroy(&lock);
    return 0;
}