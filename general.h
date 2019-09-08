#ifndef __GENERAL_H__
#define __GENERAL_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ctype.h>

#define MAX_LEN 80
#define SERV_PORT 10086
#define SERV_IP "127.0.0.1"

typedef struct
{
    bool heart_beat;
    uint8_t ctrl_code;
}ctrl_t

#endif