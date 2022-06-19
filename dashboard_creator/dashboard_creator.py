#!/usr/bin/python

import requests
import json
import logging
import argparse
import pymysql
import time
import configparser
import copy

headers = {'Accept': 'application/json', 'Content-Type': 'application/json; charset=UTF-8'}
grafana_conatiner_name = 'grafana_container'
global connection

def get_new_dashboards()->dict:
    new_dashboards = {}
    with connection.cursor() as cursor:
        sql = "SELECT id, source_name FROM data_source"
        cursor.execute(sql)
        sources = cursor.fetchall()
        print("Sources: ", sources)
        for source in sources:
            print(source)
            print(f"http://admin:adminpw@{grafana_conatiner_name}:3000/api/dashboards/{source['source_name']}")
            response = requests.get(f"http://admin:adminpw@{grafana_conatiner_name}:3000/api/search?query={source['source_name']}", headers=headers)
            print(response.json())
            if not response.json():
                new_dashboards[source['id']] = source['source_name']
    return new_dashboards


def get_panels(source_id)->dict:
    raw_sql = {}
    with connection.cursor() as cursor:
        sql = f"SELECT id, field_name FROM data_field WHERE source_id={source_id}"
        cursor.execute(sql)
        fields = cursor.fetchall()
        for field in fields:
            raw_sql[field['field_name']] = "SELECT UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) as time, field_value as value FROM data_main WHERE (UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) BETWEEN ${__from:date:seconds} AND ${__to:date:seconds}) AND data_main.field_id = %d ORDER BY date ASC;" % int(field['id'])
            print(field['field_name'],":",raw_sql[field['field_name']])
    return raw_sql


def get_next_panel_id()->int:
    response = requests.get(f"http://admin:adminpw@{grafana_conatiner_name}:3000/api/search?query={source['source_name']}", headers=headers)
    pass


def add_new_dashboards(dashboards, template)->None:
    for source_id in dashboards:
        fields = get_panels(source_id)
        if len(template["dashboard"]["panels"]) == 0:
            logging.error('template has no panels')
            exit(-1)
        panel_template = template["dashboard"]["panels"][0]
        if len(panel_template["targets"][0]["rawSql"]) == 0:
            logging.error('template has no raw sql')
            exit(-1)
        template["dashboard"]["panels"] = []
        panel_id = 1
        for title in fields:
            print(type(template["dashboard"]["panels"]))
            print(title)
            panel_temp = copy.deepcopy(panel_template)
            panel_temp["title"] = title
            panel_temp["targets"][0]["rawSql"] = fields[title]
            panel_temp["gridPos"]["y"] = (panel_id - 1) * 8
            panel_temp["id"] = panel_id
            panel_id += 1
            template["dashboard"]["panels"].append(panel_temp)
        template["dashboard"]["title"] = dashboards[source_id]
        print(template["dashboard"]["panels"])
        response = requests.post(f'http://admin:adminpw@{grafana_conatiner_name}:3000/api/dashboards/db', headers=headers, json=template)
        print(response.status_code, response.content)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--template_path', type=str, default='templates/basic_template.json', help='path to template json file')
        parser.add_argument('--cfg_path', type=str, default='configs/config.ini', help='path to cfg file with settings')

        args = parser.parse_args()
        template_path = args.template_path
        if not template_path:
            logging.error('no path to template file')
            exit(-1)

        config_path = args.cfg_path
        if not config_path:
            logging.error('no path to config file')
            exit(-1)

        config = configparser.ConfigParser()
        config.read(config_path)

        connection = pymysql.connect(host=config['MySQL']['host'],
                                     user=config['MySQL']['user'],
                                     password=config['MySQL']['password'],
                                     database=config['MySQL']['database'],
                                     port=int(config['MySQL']['port']),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)

        dashboard_template = {}
        with open(template_path, 'r') as dashboard_template_file:
            template = json.load(dashboard_template_file)
            print(type(template))
            print(template)

        interval = int(config["OTHER"]["interval"])
        if not interval:
            interval = 300 # 2 minutes default
        while True:
            print(time.strftime("%H:%M:%S", time.localtime()), 'start')
            dashboards = get_new_dashboards()
            if dashboards:
                add_new_dashboards(dashboards,template)
            print(time.strftime("%H:%M:%S", time.localtime()), 'end')
            time.sleep(interval)
    except Exception as e:
        print(e)
        exit(-1)
