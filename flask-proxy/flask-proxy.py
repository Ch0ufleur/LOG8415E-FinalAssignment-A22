# LOG8415E - Final assignment
# Author: Jimmy Bell
# Flask server acting as a proxy with REST implementation

from flask import Flask
from flask import request
import pymysql
from sshtunnel import SSHTunnelForwarder
import random

DATABASE_U = 'finaltp'
DATABASE_P = ''

app = Flask(__name__)

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
    app.config['master_ip'] = master_ip
    app.config['node2_ip'] = node2_ip
    app.config['node3_ip'] = node3_ip
    app.config['node4_ip'] = node4_ip
    print('Proxy configured with following IPs: master: ', app.config['master_ip'], ' node2: ', app.config['node2_ip'], ' node3: ', app.config['node3_ip'], ' node4: ', app.config['node4_ip'])
    return app

def do_query_default(q:str) -> str:
    """
    Performs the query directly on the management node by connecting to it directly with pymysql. There is no need to use a ssh tunnel for this implementation.

    Parameters:
    q: query to perform

    Returns:
    query_result: the result of the query
    """
    connection = pymysql.connect(host=app.config['master_ip'], user='finaltp', password='', database='sakila', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    query_result = ''
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(q)
            query_result = cursor.fetchall()
        connection.commit()
    return str(query_result)

@app.route("/default", methods=['GET'])
def default():
    """
    Route for Direct Hit proxy implementation
    
    Parameters:

    Returns:
    response: The result of the query
    """
    query:str = request.args.get('query')
    response = app.response_class(response=do_query_default(query), status=200, mimetype='text/html')
    return response

@app.route("/random", methods=['GET'])
def random():
    """
    Route for Random proxy implementation
    
    Parameters:

    Returns:
    response: The result of the query
    """
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(response=do_query_random(query), status=200, mimetype='text/html')
    return response

@app.route("/ping", methods=['GET'])
def ping():
    """
    Route for the custom proxy implementation, which select the node with the smallest ping to forward the request to
    
    Parameters:

    Returns:
    response: The result of the query
    """
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(response=do_query_ping(query), status=200, mimetype='text/html')
    return response

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
    app.run(debug=True)

def do_query_random(q:str):
    """
    Performs the query on a random data node.

    Parameters:
    q: query to perform

    Returns:
    query_result: the result of the query
    """
    if 'select'!=q[0:6].lower: # If it is not a select, then we perform on the master node
        return do_query_default(q)
    node_id = str(random.randInt(2,5)) # Values from 2 to 4 inclusive
    print("selected data node ",node_id, " at random")
    query_result = ''
    with sshtunnel.open_tunnel(
        (app.config['master_ip'], 22),
        ssh_username="ubuntu",
        ssh_pkey="/home/ubuntu/standa2.pem",
        remote_bind_address=(?, 22),
        local_bind_address=('0.0.0.0', 10022)
    ) as tunnel:
        connection = pymysql.connect(host=app.config['master_ip'], user='finaltp', password='', database='sakila', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, bind_address=?)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(q)
                query_result = cursor.fetchall()
            connection.commit()
    
    return str(query_result)

def do_query_ping(q:str):
    """
    Performs the query on the data node with the least latency

    Parameters:
    q: query to perform

    Returns:
    query_result: the result of the query
    """
    if 'select'!=q[0:6].lower: # If it is not a select, then we perform on the master node
        return do_query_default(q)
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