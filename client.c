#include "general.h"

int init_socket()
{
    int sockfd = 0;
    struct sockaddr_in addr;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
    {
        perror("socket() failed.");
        return -1;
    }

    if(inet_pton(AF_INET, SERV_IP, &addr.sin_addr)<=0)
    {
        perror("Server Address Error.");
        return -1;
    }
    addr.sin_family = AF_INET;
    addr.sin_port = htons(SERV_PORT);

    if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("connection failed.");
        return -1;
    }

    return sockfd;
}

int main(int argc, char const *argv[]) 
{ 
    int sockfd = 0, res;
    ctrl_t ctrl_msg = {0};

    if ((sockfd = init_socket()) < 0)
    {
        exit(0);
    }

    printf("Now on!");

    while(1)
    {
        res = read(sockfd, &ctrl_msg, sizeof(ctrl_t));
        printf("received once.\n");
    }
    
    return 0; 
}