#!/bin/bash

while true; do
    read -p "Do you wish to remove ALL docker containers and images?(y/n) " yn
    case $yn in
        [Yy]* ) 
			sudo docker stop grafana_container; 
			sudo docker stop app_container; 
			sudo docker stop mysql_container; 
			sudo docker rm grafana_container --force; 
			sudo docker rm app_container --force; 
			sudo docker rm mysql_container --force;
			sudo docker rmi grafana/grafana --force; 
			sudo docker rmi app --force; 
			sudo docker rmi mysql --force;
			sudo docker system prune -y;
			break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done




