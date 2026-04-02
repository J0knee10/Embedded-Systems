#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <time.h>

void run_client(char *hostname, int port, int id) {
    int sockfd, n, send_num, recv_num;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    server = gethostbyname(hostname);
    
    memset((char *) &serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(port);

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) return;

    // Challenge: Random number generation
    srand(time(NULL) ^ (getpid() << 16));
    send_num = rand() % 20; 

    printf("Client Child [%d] (PID %d): Sending %d\n", id, getpid(), send_num);
    write(sockfd, &send_num, sizeof(int));
    
    read(sockfd, &recv_num, sizeof(int));
    printf("Client Child [%d]: Received from Server: %d\n", id, recv_num);

    close(sockfd);
}

int main(int argc, char *argv[]) {
    if (argc < 3) { fprintf(stderr,"usage %s hostname port\n", argv[0]); exit(1); }

    for (int i = 1; i <= 3; i++) {
        if (fork() == 0) { // Child process
            run_client(argv[1], atoi(argv[2]), i);
            exit(0); 
        }
    }
    // Parent waits for children
    for (int i = 0; i < 3; i++) wait(NULL);
    return 0;
}