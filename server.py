import peeweedbevolve
import os
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db
from models import *

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command()
def migrate():
   db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   flash("hey")
   return render_template('index.html')

#STORE

@app.route("/store", methods=["GET"])
def store():
   return render_template('store.html')

@app.route("/store/new", methods=["POST"])
def create_store():
   store = Store(name=request.form['name'])
   if store.save():
      flash("Store succesfully added")
   else:
      flash("Not succesfull, try again.")
   return redirect(url_for('store'))

@app.route("/store/<int:id>", methods=["GET"])
def show_store(id):
   store = Store.get_by_id(id)
   return render_template('store_show.html', store=store)   

#Warehouse

@app.route("/warehouse", methods=["GET"])
def warehouse():
   stores = Store.select()
   return render_template('warehouse.html', stores=stores)

@app.route("/warehouse/new", methods=["POST"])
def create_warehouse():
   store = Store.get(
      id=request.form["store_id"]
   )
   warehouse = Warehouse(
      location = request.form["location"],
      store=store
   )

   if warehouse.save():
      flash("Warehouse added to store!")
   else:
      flash("Unable to add warehouse!")
   return redirect(url_for("warehouse"))

#Product

@app.route("/product", methods=["GET"])
def product():
   return render_template('product.html')

if __name__ == '__main__':
   app.run(debug=True)