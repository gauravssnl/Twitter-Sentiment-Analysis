from flask import Flask, render_template, redirect, url_for, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required

import analyse
import sentiment_probability

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class HashtagForm(FlaskForm):
    hashtag = StringField('Enter hashtag query', validators=[Required()])
    limit = IntegerField('Enter number of tweets', validators=[Required()])
    submit = SubmitField('Submit')


class TextForm(FlaskForm):
    text = StringField('Enter input text', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    hashtag = None
    form = HashtagForm()
    limit = None
    if form.validate_on_submit():
        hashtag = form.hashtag.data
        limit = form.limit.data
        form.hashtag.data = ''
        form.hashtag.limit = ''
        # return render_template('query.html', form=form, hashtag=hashtag, limit =limit)
        return redirect(url_for('sentiment', hashtag=hashtag, limit=abs(limit)))
    return render_template('index.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sentiment')
def sentiment():
    hashtag = request.args.get('hashtag', None)
    limit = request.args.get('limit', None)
    return render_template('query.html', get_tweets=analyse.get_tweets, analyse=analyse.analyse, hashtag=hashtag, limit=limit, )


@app.route('/probability', methods=['GET', 'POST'])
def probability():
    hashtag = None
    form = HashtagForm()
    limit = None
    if form.validate_on_submit():
        hashtag = form.hashtag.data
        limit = form.limit.data
        form.hashtag.data = ''
        form.hashtag.limit = ''
        # return render_template('query.html', form=form, hashtag=hashtag, limit =limit)
        return redirect(url_for('sentimentprobability', hashtag=hashtag, limit=abs(limit)))
    return render_template('index.html', form=form)


@app.route('/sentimentprobability')
def sentimentprobability():
    hashtag = request.args.get('hashtag', None)
    limit = request.args.get('limit', None)
    return render_template('query.html', get_tweets=sentiment_probability.get_tweets, analyse=sentiment_probability.analyse, hashtag=hashtag, limit=limit)


@app.route('/text', methods=['GET', 'POST'])
def text():
    string = None
    form = TextForm()
    if form.validate_on_submit():
        string = form.text.data
        form.text.data = ''
        # return redirect(url_for('textresult', string=string))
        return render_template('textresult.html', string=string, analyse=sentiment_probability.analyse_string)
    return render_template('index.html', form=form)


"""
@app.route('/textresult')
def textresult():
    string = request.args.get('string', None)
    return render_template('textresult.html', analyse=sentiment_probability.analyse)
"""

if __name__ == '__main__':
    manager.run()
