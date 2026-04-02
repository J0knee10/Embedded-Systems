#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/socket.h>
#include <netinet/in.h>

sem_t thread_limit;

void* handle_request(void* arg) {
    int sock = *(int*)arg;
    int val, result;

    if (read(sock, &val, sizeof(int)) > 0) {
        result = val * 5; // The math requirement
        printf("Thread %lu: Received %d, Sending back %d\n", pthread_self(), val, result);
        write(sock, &result, sizeof(int));
    }

    close(sock);
    free(arg);
    sem_post(&thread_limit); // Leave the room (increment semaphore)
    return NULL;
}

int main(int argc, char *argv[]) {
    int sockfd, newsockfd, port;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t clilen = sizeof(cli_addr);

    if (argc < 2) exit(1);
    
    // Challenge: Limit to 3 threads
    sem_init(&thread_limit, 0, 3);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(atoi(argv[1]));

    bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    listen(sockfd, 5);

    printf("Server Active... Waiting for connections.\n");

    while (1) {
        sem_wait(&thread_limit); // Enter the room (decrement semaphore)
        
        newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr, &clilen);
        
        pthread_t tid;
        int *new_sock = malloc(sizeof(int));
        *new_sock = newsockfd;
        
        pthread_create(&tid, NULL, handle_request, new_sock);
        pthread_detach(tid); // Clean up automatically
    }

    sem_destroy(&thread_limit);
    return 0;
}