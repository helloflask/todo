# Task5
A to-do list App made with Flask and JavaScript.

## DEMO
http://task5.herokuapp.com/

![demo](https://raw.githubusercontent.com/helloflask/todo/master/static/demo.png)

## Dependency
Flask-SQLAlchemy==2.1  
SQLAlchemy==1.1.4  


## Installation
First, clone it from github:
```
git clone https://github.com/helloflask/todo.git
```
Change to app directory, use `virtualenv` create and activate virtual enviroment.  
Then use `pip` to install requirements (you may need to comment out `gunicorn`, `gevent` and `psycopg2`)：  
```
pip install -r requirements.txt
```

Comment out these lines (app.py):
```
import psycopg2
...
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
```
Uncomment this lines (app.py):
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # use in-memory database
```

Then exit python and run the app:
```
python app.py
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
