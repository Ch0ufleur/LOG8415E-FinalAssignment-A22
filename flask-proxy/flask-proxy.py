from flask import Flask
from flask import request, response
import pymysql
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

@app.route("/", methods=['GET'])
def sql_query():
    query:str = request.args.get('query')
    print(query)
    response = app.response_class(reponse=do_query(query), status=200, mimetype='application/text')
    return response

def do_query(q:str):
    server = SSHTunnelForwarder(
        'alfa.8iq.dev',
        ssh_username="pahaz",
        ssh_password="secret",
        remote_bind_address=('127.0.0.1', 8080)
    )
    connection = pymysql.connect(host=selectHost(), user='finaltp', password='', database='sakila', charset='utf8mb4', bind_address=tunnel-ip)
    with connection:
        with connection.cursor() as cursor:


def selectHost():

"""
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
""" https://pypi.org/project/sshtunnel/