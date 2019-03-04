#!/usr/bin/python
from flask import Flask, render_template
from src.model.product import Product
import mysql.connector as mariadb
import os

app = Flask(__name__)

@app.route('/')
def home():
    products = get_products()
    return render_template('home.html', products=products)

def get_products():
    print ('PYFLASKHERO_DB_USER: ' + os.environ['PYFLASKHERO_DB_USER'])
    print ('PYFLASKHERO_DB_PORT: ' + os.environ['PYFLASKHERO_DB_PORT'])
    print ('PYFLASKHERO_DB_USER: ' + os.environ['PYFLASKHERO_DB_USER'])
    print ('PYFLASKHERO_DB_PWD: ' + os.environ['PYFLASKHERO_DB_PWD'])
    print ('PYFLASKHERO_DB_NAME: ' + os.environ['PYFLASKHERO_DB_NAME'])
    mariadb_connection = mariadb.connect(host=os.environ['PYFLASKHERO_DB_HOST'],
                                         port=os.environ['PYFLASKHERO_DB_PORT'],
                                         user=os.environ['PYFLASKHERO_DB_USER'],
                                         password=os.environ['PYFLASKHERO_DB_PWD'],
                                         database=os.environ['PYFLASKHERO_DB_NAME'])
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT product_name as name, product_manufacturer as manufacturer , submission_date FROM products")
    products = []
    for name, manufacturer, submission_date in cursor:
        print('Found something')
        print('product : ' + name)
        products.append(Product(name, manufacturer, submission_date))
    for product in products:
        print(product)
    mariadb_connection.close()
    return products

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)