# -*- coding: utf-8 -*-
import os
try:
    import psycopg2  # for heroku deploy
except:
    pass

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG'] = True
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), default=1)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('Item', backref='category')


# only for local test
# @app.before_first_request
def init_db():
    """Insert default categories and demo items.
    """
    db.create_all()
    inbox = Category(name=u'收件箱')
    done = Category(name=u'已完成')
    shopping_list = Category(name=u'购物清单')
    work = Category(name=u'工作')
    item = Item(body=u'看一小时《战争与和平》')
    item2 = Item(body=u'晒太阳')
    item3 = Item(body=u'写作练习30分钟')
    item4 = Item(body=u'3瓶牛奶', category=shopping_list)
    item5 = Item(body=u'5个苹果', category=shopping_list)
    item6 = Item(body=u'12支铅笔', category=shopping_list)
    item7 = Item(body=u'浇花', category=done)
    item8 = Item(body=u'完成demo', category=work)
    db.session.add_all([inbox, done, item, item2, item3, item4, item5, item6, item7, item8])
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        body = request.form.get('item')
        category_id = request.form.get('category')
        category = Category.query.get_or_404(category_id)
        item = Item(body=body, category=category)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('category', id=category_id))
    return redirect(url_for('category', id=1))


@app.route('/category/<int:id>')
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
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/edit-category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    category.name = request.form.get('name')
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/done/<int:id>', methods=['GET', 'POST'])
def done(id):
    item = Item.query.get_or_404(id)
    category = item.category
    done_category = Category.query.get_or_404(2)
    done_item = Item(body=item.body, category=done_category)
    db.session.add(done_item)
    db.session.delete(item)
    db.session.commit()
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
    app.run()
