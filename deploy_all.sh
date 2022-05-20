#!/bin/bash

# need to start from mysql container to create network
cd docker_mysql
sudo ./deploy.sh

cd ../docker_grafana
sudo ./deploy.sh

cd ../dashboard_creator
sudo ./deploy.sh
