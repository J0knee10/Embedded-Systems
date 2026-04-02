#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/wait.h>

struct server_reply {
    int slot_index;
    int current_sum;
};

void run_child_client(char *host, int port) {
    int sockfd, val_to_send;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    struct server_reply reply;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    server = gethostbyname(host);
    
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(port);

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) return;

    // Logic: Send a value based on PID for variety
    val_to_send = getpid() % 100; 
    write(sockfd, &val_to_send, sizeof(int));
    
    // Receive structured reply
    read(sockfd, &reply, sizeof(struct server_reply));

    printf("[Client PID %d] Sent: %d | Server Slot: %d | Global Sum: %d\n", 
            getpid(), val_to_send, reply.slot_index, reply.current_sum);

    close(sockfd);
}

int main(int argc, char *argv[]) {
    if (argc < 4) { 
        printf("Usage: %s [hostname] [port] [N_children]\n", argv[0]); 
        exit(1); 
    }

    int N = atoi(argv[3]);

    for (int i = 0; i < N; i++) {
        if (fork() == 0) {
            run_child_client(argv[1], atoi(argv[2]));
            exit(0);
        }
    }

    // Parent waits for all N children
    for (int i = 0; i < N; i++) wait(NULL);
    
    return 0;
}