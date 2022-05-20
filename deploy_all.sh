#!/bin/bash

# need to start from mysql container to create network
echo "create mysql"
cd docker_mysql
sudo ./deploy.sh
echo "done mysql"

echo "create grafana"
cd ../docker_grafana
sudo ./deploy.sh
echo "done grafana"

echo "create dashboard_creator"
cd ../dashboard_creator
sudo ./deploy.sh
echo "done dashboard_creator"