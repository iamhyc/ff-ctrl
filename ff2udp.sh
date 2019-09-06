#!/bin/bash

ADDR=127.0.0.1
if [ -n $1 ]; then
    ADDR=$1;
fi

ffmpeg -f v4l2 -i "/dev/video0" \
-profile:v high -pix_fmt yuvj420p -level:v 4.1 -preset ultrafast -tune zerolatency \
-vcodec libx264 -r 30 -b:v 512k -s 640x360 \
-flush_packets 0 \
-f mpegts udp://$ADDR:1234
