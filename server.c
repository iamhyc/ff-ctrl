#include "general.h"

int init_socket()
{
    int sockfd = 0, res = 0;
    struct sockaddr_in addr;

    // socket(), Create socket file descriptor
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
    {
        perror("socket fd failed.");
        return -1
    }

    // setsockopt, Bind socket to port
    if ((setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR|SO_REUSEPORT, &res, sizeof(res))) != 0)
    {
        perror("SetSockOpt failed.");
        return -1;
    }

    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(SERV_PORT);

    // bind sockfd to port
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind failed.");
        return -1;
    }

    if ((listen(sockfd, 1)) < 0)
    {
        perror("listen failed.");
        return -1;
    }

    return sockfd;
}

int main(int argc, char const *argv[])
{
    int sockfd,c_sockfd;
    struct sockaddr_in addr;
    ctrl_t ctrl_msg = {0};
    
    if ((sockfd = init_socket()) < 0)
    {
        exit(0);
    }

    if ((c_sockfd = accept(sockfd, &addr, sizeof(addr))) < 0)
    {
        perror("accept failed.");
        exit(0);
    }
    printf("From %s:%d", inet_ntoa(addr.sin_addr), nstoh(addr.sin_port));
    
    while(1)
    {
        sleep(1);
        if (send(client_sockfd, ctrl_msg, sizeof(ctrl_t), 0) < 0)
        {
            perror("Packet Loss.");
        }
    }

    close(c_sockfd);
    close(sockfd);
    return 0;
}