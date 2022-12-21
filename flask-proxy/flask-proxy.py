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
    connection = pymysql.connect(host=selectHost(), user='finaltp', password='', database='sakila', charset='utf8mb4', bind_address=tunnel-ip)
    with connection:
        with connection.cursor() as cursor:


def selectHost():

