from flask import Flask, render_template, redirect, url_for, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required

from analyse import get_tweets, analyse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    hashtag = StringField('Enter hashtag query', validators=[Required()])
    limit = IntegerField('Enter number of tweets', validators=[Required()])
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
    form = NameForm()
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
    return render_template('query.html', get_tweets=get_tweets, analyse=analyse, hashtag=hashtag, limit=limit, )


if __name__ == '__main__':
    manager.run()
