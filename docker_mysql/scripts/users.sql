USE incoming_data;

# create cli user and grant rights
CREATE USER 'cli'@'localhost' IDENTIFIED BY 'clipw';
GRANT ALL PRIVILEGES ON *.* TO 'cli'@'localhost';

# create grafana user and grant rights
CREATE USER 'grafana'@'statistics_gather' IDENTIFIED BY 'grafanapw';
GRANT SELECT ON `incoming_data`.* TO 'grafana'@'statistics_gather';

# create app user and grant rights
CREATE USER 'app'@'statistics_gather' IDENTIFIED BY 'apppw';
GRANT ALL PRIVILEGES ON `incoming_data`.* TO 'app'@'statistics_gather';


