# LOG8415E - Final assignment
# Author: Jimmy Bell
# Flask server acting as a proxy with REST implementation

from flask import Flask
from flask import request
import pymysql
import subprocess
from sshtunnel import SSHTunnelForwarder
import random

DATABASE_U = 'finaltp'
DATABASE_P = ''

app = Flask(__name__)

# https://stackoverflow.com/a/48349994/13775984
def create_app(master_ip, node2_ip, node3_ip, node4_ip, proxy):
    """
    Instantiates the server app with the appropriate configuration
    
    Parameters:
    master_ip: Local IP address of the management node
    node2_ip: Local IP address of the second node, which is a data node
    node3_ip: Local IP address of the third node, which is a data node
    node4_ip: Local IP address of the fourth node, which is a data node
    proxy: internal IP of the proxy

    Returns:
    app: The instantiated and properly configured app
    """
    app.config['master_ip'] = master_ip
    app.config['node2_ip'] = node2_ip
    app.config['node3_ip'] = node3_ip
    app.config['node4_ip'] = node4_ip
    app.config['proxy_ip'] = proxy
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

def execute_forwarded_query_on_node(node_id, q) -> str:
    """
    Performs a query via the ssh tunnel on specified data node

    Parameters:
    node_id: the id to perform the query on

    Return:
    query_result: the result of the query
    """
    with SSHTunnelForwarder(
        (app.config['node'+node_id+'_ip'], 22), #Connecting to the chosen data node
        ssh_username="ubuntu",
        ssh_pkey="/home/ubuntu/standa2.pem",
        remote_bind_address=(app.config['master_ip'], 3306) #Binding to the mysql engine on the master node
    ) as tunnel:
    #Performing the request
        connection = pymysql.connect(host='127.0.0.1', port=tunnel.local_bind_port, user='finaltp', password='', database='sakila', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(q)
                query_result = cursor.fetchall()
            connection.commit()
    return query_result

def do_query_random(q:str):
    """
    Performs the query on a random data node.

    Parameters:
    q: query to perform

    Returns:
    query_result: the result of the query
    """
    if 'select'!=q[0:6].lower(): # If it is not a select, then we perform on the master node
        return do_query_default(q)
    node_id = str(random.randint(2,4)) # Values from 2 to 4 inclusive
    print("selected data node ",node_id, " at random")
    query_result = execute_forwarded_query_on_node(node_id,q)
    return str(query_result)

@app.route("/random", methods=['GET'])
def randomize():
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

def ping_instance(node_ip):
    """
    Pings an instance and returns the response time

    Parameters:
    node_ip: ip of the node to ping

    Returns
    response_time: response time after doing the ping command
    """
    response = subprocess.run(["ping", "-c", "1", node_ip], capture_output=True)
    output = response.stdout.decode("utf-8")
    response_time = output.split("time=")[1].split(" ms")[0]
    return response_time

def do_query_ping(q:str):
    """
    Performs the query on the data node with the least latency

    Parameters:
    q: query to perform

    Returns:
    query_result: the result of the query
    """
    if 'select'!=q[0:6].lower(): # If it is not a select, then we perform on the master node
        return do_query_default(q)

    smallest_ping = ping_instance(app.config['node2_ip'])
    n2_ping = smallest_ping
    print("n2 ping ", n2_ping)
    n3_ping = ping_instance(app.config['node3_ip'])
    if n3_ping<smallest_ping:
        smallest_ping = n3_ping
    print("n3 ping ", n3_ping)
    n4_ping = ping_instance(app.config['node4_ip'])
    if n4_ping<smallest_ping:
        smallest_ping = n4_ping
    print("n4 ping ", n4_ping)
    times = {'2':n2_ping, '3':n3_ping, '4':n4_ping}
    node = min(times, key=lambda key: times[key])
    print("selected data node ",node, " with less ping!")
    query_result = execute_forwarded_query_on_node(node,q)
    return str(query_result)

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
    parser.add_argument('-proxy')
    args = parser.parse_args()
    m = args.m
    n2 = args.n2
    n3 = args.n3
    n4 = args.n4
    proxy = args.proxy
    app = create_app(m,n2,n3,n4, proxy)
    app.run(host=app.config['proxy_ip'])