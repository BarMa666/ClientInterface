#!/bin/bash

while true; do
    read -p "Do you wish to remove ALL docker containers and images?(y/n) " yn
    case $yn in
        [Yy]* ) 
			sudo docker stop $(sudo docker ps -a -q); 
			sudo docker rm $(sudo docker ps -a -q) --force; 
			sudo docker rmi $(sudo docker images -a -q) --force; 
			sudo docker volume prune --force; 
			sudo docker system prune --force; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done




