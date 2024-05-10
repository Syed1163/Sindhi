from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
import json
from flask import render_template

app = Flask(__name__)
app.secret_key = 'ABCDDD123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test1234@db/mysql'

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(50))
    supplier = db.Column(db.String(200))
    price = db.Column(db.String(10))

    def __init__(self, name, description, supplier, price):
        self.name = name
        self.description = description
        self.supplier = supplier
        self.price = price


@app.route('/show_all')
def show_all():
    return render_template('show_all.html', products=Product.query.all())


@app.route('/')
def show():
    db.create_all()
    print("Welcome")
    return "Welcome"


@app.route('/show_new')
def show_new():
    return render_template('newproduct.html')


@app.route('/new_prod', methods=['POST', 'GET'])
def new_prod():
    if request.method == 'POST':
        product = Product(request.form['name'], request.form['description'], request.form['supplier'], request.form['price'])
        db.session.add(product)
        db.session.commit()
    return render_template('show_all.html', products=Product.query.all())


@app.route('/update_prod', methods=['POST', 'GET'])
def update_prod():
    if request.method == 'POST':
        print
        "Inside POST"
        try:
            id = request.form['id']
            product = Product.query.filter_by(id=id).first()
            product.name = request.form['name']
            product.description = request.form['description']
            product.supllier = request.form['supllier']
            product.price = request.form['price']
            db.session.commit()
        except:
            msg = "error during update operation"
            print
            msg
    return render_template('show_all.html', products=Product.query.all())


@app.route('/show_update', methods=['POST', 'GET'])
def show_update():
    id = request.args.get('id')
    product = Product.query.filter_by(id=id).first()
    return render_template('update_prod.html', product=product)


@app.route('/delete_prod')
def delete_prod():
    id = request.args.get('id')
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    return render_template('show_all.html', products=Product.query.all())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
