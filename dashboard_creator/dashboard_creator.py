#!/usr/bin/python

import requests
import json
import logging
import argparse
import pymysql
import time
import configparser

headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer eyJrIjoiQjlqTG50cHJna2NOR2JCOUJjYUNFdm5scTdOQzRZYXAiLCJuIjoidXBkYXRlciIsImlkIjoxfQ=='}


def get_new_dashboards()->dict:
    new_dashboards = []
    with connection.cursor() as cursor:
        sql = "SELECT id, source_name FROM data_source"
        cursor.execute(sql)
        sources = cursor.fetchall()
        for id, source_name in sources:
            print(source_name)
            response = requests.get(f'https://late-beans-mate-90-188-10-160.loca.lt/api/dashboards/{source_name}', headers=headers)
            if response.status_code != 200:
                new_dashboards[id] = source_name
    return new_dashboards


def get_panels(source_id)->dict:
    raw_sql = {}
    with connection.cursor() as cursor:
        sql = f"SELECT id, field_name FROM data_field WHERE source_id={source_id}"
        cursor.execute(sql)
        for id, field_name in cursor.fetchall():
            raw_sql[field_name] = f"SELECT UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) as time, field_value as value FROM data_main WHERE (UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) BETWEEN ${__from:date:seconds} AND ${__to:date:seconds}) AND data_main.field_id = {id} ORDER BY date ASC;"
    return raw_sql


def add_new_dashboards(dashboards, template)->None:
    for source_id, source_name in dashboards:
        raw_sql = get_panels(source_id)
        for title, sql_request in raw_sql:
            template["panels"]["title"] = title
            template["panels"]["targets"]["rawSql"] = sql_request
        template["title"] = source_name
        response = requests.post('https://late-beans-mate-90-188-10-160.loca.lt/api/dashboards/db', headers=headers, json=template)
        print(response.content)


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

        print(template_path)
        print(config_path)

        config = configparser.ConfigParser()
        config.read(config_path)
        print(config['MySQL']['host'])
        print(config['MySQL']['user'])
        print(config['MySQL']['password'])
        print(config['MySQL']['database'])
        print(config['MySQL']['port'])

        connection = pymysql.connect(host=config['MySQL']['host'],
                                     user=config['MySQL']['user'],
                                     password=config['MySQL']['password'],
                                     database=config['MySQL']['database'],
                                     port=int(config['MySQL']['port']),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        dashboard_template = {}
        with open(template_path, 'r') as dashboard_template_file:
            template = json.load(dashboard_template_file)
            print(template)

        interval = int(config["OTHER"]["interval"])
        if not interval:
            interval = 300 # 2 minutes default
        while True:
            print('start')
            dashboards = get_new_dashboards()
            if dashboards:
                add_new_dashboards(dashboards,template)
            print('end')
            time.sleep(interval)
    except Exception as e:
        print(e)
        exit(-1)
