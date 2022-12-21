# LOG8415E - Final assignment
# Author: Jimmy Bell
# 

from flask import Flask
from flask import request
import pymysql
from sshtunnel import SSHTunnelForwarder

# https://stackoverflow.com/a/48349994/13775984
def create_app(master_ip, node2_ip, node3_ip, node4_ip):
    """
    Instantiates the server app with the appropriate configuration
    
    Parameters:
    master_ip: Local IP address of the management node
    node2_ip: Local IP address of the second node, which is a data node
    node3_ip: Local IP address of the third node, which is a data node
    node4_ip: Local IP address of the fourth node, which is a data node

    Returns:
    app: The instantiated and properly configured app
    """
    app = Flask(__name__)
    app.config['master_ip'] = master_ip
    app.config['node2_ip'] = node2_ip
    app.config['node3_ip'] = node3_ip
    app.config['node4_ip'] = node4_ip
    print('Proxy configured with following IPs: master: ', app.config['master_ip'], ' node2: ', app.config['node2_ip'], ' node3: ', app.config['node3_ip'], ' node4: ', app.config['node4_ip'])
    return app

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-m')
  parser.add_argument('-n2')
  parser.add_argument('-n3')
  parser.add_argument('-n4')
  args = parser.parse_args()
  m = args.m
  n2 = args.n2
  n3 = args.n3
  n4 = args.n4
  app = create_app(m,n2,n3,n4)
  app.run()

@app.route("/default", methods=['GET'])
def sql_query():
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(reponse=do_query_default(query), status=200, mimetype='application/text')
    return response

@app.route("/random", methods=['GET'])
def sql_query():
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(reponse=do_query_random(query), status=200, mimetype='application/text')
    return response

@app.route("/ping", methods=['GET'])
def sql_query():
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(reponse=do_query_ping(query), status=200, mimetype='application/text')
    return response

def do_query_default(q:str):
    server = SSHTunnelForwarder(
        'alfa.8iq.dev',
        ssh_username="pahaz",
        ssh_password="secret",
        remote_bind_address=('127.0.0.1', 8080)
    )
    connection = pymysql.connect(host=app.config['master_ip'], user='finaltp', password='', database='sakila', charset='utf8mb4', bind_address=tunnel-ip)
    with connection:
        with connection.cursor() as cursor:
            a

def do_query_random(q:str):
    server = SSHTunnelForwarder(
        'alfa.8iq.dev',
        ssh_username="pahaz",
        ssh_password="secret",
        remote_bind_address=('127.0.0.1', 8080)
    )
    connection = pymysql.connect(host=select_random(), user='finaltp', password='', database='sakila', charset='utf8mb4', bind_address=tunnel-ip)
    with connection:
        with connection.cursor() as cursor:
            a

def do_query_ping(q:str):
    server = SSHTunnelForwarder(
        'alfa.8iq.dev',
        ssh_username="pahaz",
        ssh_password="secret",
        remote_bind_address=('127.0.0.1', 8080)
    )
    connection = pymysql.connect(host=select_minimal_ping(), user='finaltp', password='', database='sakila', charset='utf8mb4', bind_address=tunnel-ip)
    with connection:
        with connection.cursor() as cursor:
            a
"""
def select_random():

def select_minimal_ping():

from sshtunnel import open_tunnel
from time import sleep

with open_tunnel(
    ('localhost', 2222),
    ssh_username="vagrant",
    ssh_password="vagrant",
    remote_bind_address=('127.0.0.1', 3306)
) as server:

    print(server.local_bind_port)
    while True:
        # press Ctrl-C for stopping
        sleep(1)

print('FINISH!')https://pymysql.readthedocs.io/en/latest/user/examples.html
https://pypi.org/project/sshtunnel/"""