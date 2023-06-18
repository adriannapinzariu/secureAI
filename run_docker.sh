#!/bin/bash
sudo docker run -it --rm  \
    --net=host  \
    --privileged \
    --runtime=nvidia \
    -v `pwd`/image_matching:/usr/src/app/image_matching \
    -v `pwd`:/usr/src/app/secureAI \
    -v `pwd`/../data:/usr/src/app/data \
    --shm-size 8G \
    secureai "$@"