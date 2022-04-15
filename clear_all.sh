#!/bin/bash

while true; do
    read -p "Do you wish to remove ALL docker containers and images?(y/n) " yn
    case $yn in
        [Yy]* ) sudo docker stop $(docker ps -a -q); sudo docker rm $(docker ps -a -q); sudo docker rmi $(docker images -a -q); break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done




