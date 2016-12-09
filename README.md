# Task5
A to-do list App made with Flask and JavaScript.

## DEMO
http://task5.herokuapp.com/

![demo](https://raw.githubusercontent.com/helloflask/todo/master/static/demo.png)

## Extensions
Flask-Script==2.0.5  
Flask-SQLAlchemy==2.1  
SQLAlchemy==1.1.4  


## Installation
First, clone it from github:
```
git clone https://github.com/helloflask/todo.git
```
Change to app directory, use `virtualenv` create and activate virtual enviroment.  
Then use `pip` to install requirements (you may need delete `gunicorn`, `gevent` and `psycopg2`)：  
```
pip install -r requirements.txt
```

Comment out this line (app.py):
```
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
```
Uncomment this lines (app.py):
```
app.config['SQLALCHEMY_DATABASE_URI'] = \
  'sqlite:///' + os.path.join(basedir, 'data.sqlite')
```

Initialize database and create two base categories (i.e. inbox and done):
```
python app.py shell
>>> from app import db, Category
>>> db.create_all()
>>> db.session.commit()
>>> inbox = Category(name='Inbox')
>>> done = Category(name='Done')
>>> db.session.add(inbox)
>>> db.session.add(done)
>>> db.session.commit()
```

Then exit python and run the app use Flask-Script's `runserver` command:
```
python app.py runserver
```

Now Go to http://127.0.0.1:5000/

## To do list
- Drag to sort items
- Edit category
- Set task's priority
- Set task's date

## More details
关于这个项目的详细介绍：[Flask实践：待办清单](https://zhuanlan.zhihu.com/p/23834410)  
更多关于Flask的原创优质内容，欢迎关注[Hello, Flask!——知乎专栏](https://zhuanlan.zhihu.com/flask)

## License
This demo application is licensed under the MIT license: http://opensource.org/licenses/mit-license.php
