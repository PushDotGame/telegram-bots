from flask import (Flask, render_template)
from libs.GroupBotORM import *
from conf import bot as be

app = Flask(__name__)

topics = Topic.select()

session_name = be.BOT_SESSION_NAME
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def index():
    return render_template('index.html', session_name=session_name, topics=topics)


@app.route('/topic/<topic_id>')
def user_page(topic_id):
    topic = Topic.get(id=topic_id)
    print('topic:', topic)

    return render_template('topic.html', session_name=session_name, topic=topic)
