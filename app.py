from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser


home = expanduser('~')
#mypkey = paramiko.RSAKey.from_private_key_file(home + pkeyfilepath)
# if you want to use ssh password use - ssh_password='your ssh password', below


sql_hostname = 'localhost'
sql_username = 'kvsekhar'
sql_password = 'Database@183'
sql_main_database = 'vc_ds'
sql_port = 3306
ssh_host = '81.201.138.98.srvlist.ukfast.net'
ssh_user = 'veerasrv'
ssh_port = 2020
ssh_password = 'Server183'
#sql_ip = '1.1.1.1.1'


app = Flask(__name__)

df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                   'B': [5, 6, 7, 8, 9],
                   'C': ['a', 'b', 'c--', 'd', 'e']})


@app.route('/', methods=("POST", "GET"))
def index():
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                passwd=sql_password, db=sql_main_database,
                port=tunnel.local_bind_port)
        query = '''SELECT * from Endole_data where `Company Registered Number` LIKE '10000005';'''
        data = pd.read_sql_query(query, conn)
        conn.close()
    return data.to_json()


if __name__ == '__main__':
    app.run()