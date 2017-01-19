# -*- coding: utf-8 -*-
import os
import psycopg2  # for heroku deploy

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret string'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#   'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# the database address below is for heroku postgres, if you want test it on local, use above address instead.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['DEBUG'] = True
manager = Manager(app)
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    location = db.Column(db.Integer, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.Integer, unique=True)
    items = db.relationship('Item', backref='category', lazy='dynamic')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        body = request.form.get('item')
        id = request.form.get('category')
        category = Category.query.get_or_404(id)
        item = Item(body=body, category=category)
        db.session.add(item)
        return redirect(url_for('category', id=id))
    return redirect(url_for('category', id=1))


@app.route('/category/<int:id>', methods=['GET', 'POST'])
def category(id):
    category = Category.query.get_or_404(id)
    categories = Category.query.all()
    items = category.items
    return render_template('index.html', items=items,
                           categories=categories, category_now=category)


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    name = request.form.get('name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/edit-item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    category = item.category
    item.body = request.form.get('body')
    db.session.add(item)
    return redirect(url_for('category', id=category.id))


@app.route('/edit-category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    category.name = request.form.get('name')
    db.session.add(category)
    return redirect(url_for('category', id=category.id))


@app.route('/done/<int:id>', methods=['GET', 'POST'])
def done(id):
    item = Item.query.get_or_404(id)
    category = item.category
    done_category = Category.query.get_or_404(2)
    done_item = Item(body=item.body, category=done_category)
    db.session.add(done_item)
    db.session.delete(item)
    return redirect(url_for('category', id=category.id))


@app.route('/delete-item/<int:id>')
def del_item(id):
    item = Item.query.get_or_404(id)
    category = item.category
    if item is None:
        return redirect(url_for('category', id=1))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/delete-category/<int:id>')
def del_category(id):
    category = Category.query.get_or_404(id)
    if category is None or id in [1, 2]:
        return redirect(url_for('category', id=1))
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category', id=1))


if __name__ == '__main__':
    manager.run()
