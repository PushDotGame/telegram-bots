from flask_bootstrap import Bootstrap
from flask import (Flask, request, redirect, url_for, render_template)
from libs.GroupBotORM import *
from conf import bot as be

bootstrap = Bootstrap()

app = Flask(__name__)
bootstrap.init_app(app)


@app.route('/')
def show_topics():
    topics = (Topic
              .select(Topic, fn.Count(Ask.id).alias('ask_count'), fn.Count(Reply.id).alias('reply_count'))
              .join(Ask, JOIN.LEFT_OUTER)
              .switch(Topic)
              .join(Reply, JOIN.LEFT_OUTER)
              .group_by(Topic)
              )
    return render_template('topics.html', session_name=be.BOT_SESSION_NAME, topics=topics)


@app.route('/topic/<topic_id>')
def show_topic(topic_id):
    topic = Topic.get(id=topic_id)
    return render_template('topic.html', session_name=be.BOT_SESSION_NAME, topic=topic)


@app.route('/add-topic', methods=['POST'])
def add_topic():
    if len(request.form['title'].strip()) > 0:
        topic = Topic.create(
            active=request.form['active'] == 'True',
            use_reply=request.form['useReply'] == 'True',
            show_title=request.form['showTitle'] == 'True',
            title=request.form['title'].strip(),
            remark=request.form['remark'].strip(),
        )
    return redirect(request.referrer)


@app.route('/update-topic/<topic_id>', methods=['POST'])
def update_topic(topic_id):
    topic = Topic.get(id=topic_id)
    topic.active = request.form['active'] == 'True'
    topic.use_reply = request.form['useReply'] == 'True'
    topic.show_title = request.form['showTitle'] == 'True'
    topic.title = request.form['title'].strip()
    topic.remark = request.form['remark'].strip()
    topic.save()
    return redirect(request.referrer)


@app.route('/add-ask', methods=['POST'])
def add_ask():
    topic = Topic.get(id=int(request.form['topic_id']))

    if len(request.form['words'].strip()) > 0:
        Ask.create(
            topic=topic,
            active=request.form['active'] == 'True',
            mode=int(request.form['mode'].strip()),
            words=request.form['words'].strip(),
            max=int(request.form['max'].strip()),
            remark=request.form['remark'].strip(),
        )
    return redirect(request.referrer)


@app.route('/update-ask/<ask_id>', methods=['POST'])
def update_ask(ask_id):
    ask = Ask.get(id=ask_id)
    ask.active = request.form['active'] == 'True'
    ask.mode = int(request.form['mode'].strip())
    ask.words = request.form['words'].strip()
    ask.max = int(request.form['max'].strip())
    ask.remark = request.form['remark'].strip()
    ask.save()
    return redirect(request.referrer)


@app.route('/add-reply', methods=['POST'])
def add_reply():
    topic = Topic.get(id=int(request.form['topic_id']))

    if len(request.form['text'].strip()) > 0:
        Reply.create(
            topic=topic,
            active=request.form['active'] == 'True',
            text=request.form['text'].strip(),
            trigger=request.form['trigger'].strip(),
            remark=request.form['remark'].strip(),
        )
    return redirect(request.referrer)


@app.route('/update-reply/<reply_id>', methods=['POST'])
def update_reply(reply_id):
    reply = Reply.get(id=reply_id)
    reply.active = request.form['active'] == 'True'
    reply.text = request.form['text'].strip()
    reply.trigger = request.form['trigger'].strip()
    reply.remark = request.form['remark'].strip()
    reply.save()
    return redirect(request.referrer)


@app.route('/kvs')
def show_kvs():
    kvs = KeyValue.select()
    return render_template('kvs.html', session_name=be.BOT_SESSION_NAME, kvs=kvs)


@app.route('/update-kv/<kv_id>', methods=['POST'])
def update_kv(kv_id):
    kv = KeyValue.get(id=kv_id)
    kv.key = request.form['key'].strip()
    kv.value = request.form['value'].strip()
    kv.save()
    return redirect(request.referrer)


app.run(debug=be.DEBUG_MODE)
