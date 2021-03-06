USE incoming_data;

-- create cli user and grant rights
-- CREATE USER 'cli'@'%' IDENTIFIED BY 'clipw';
-- GRANT ALL PRIVILEGES ON *.* TO 'cli'@'%';

-- create grafana user and grant rights
CREATE USER 'grafana'@'%' IDENTIFIED BY 'grafanapw';
GRANT SELECT ON `incoming_data`.* TO 'grafana'@'%';

-- create grafana user and grant rights
CREATE USER 'dashboard_creator'@'%' IDENTIFIED BY 'dbcpw';
GRANT SELECT ON `incoming_data`.* TO 'dashboard_creator'@'%';

-- create app user and grant rights
CREATE USER 'app'@'%' IDENTIFIED BY 'apppw';
GRANT ALL PRIVILEGES ON `incoming_data`.* TO 'app'@'%';


