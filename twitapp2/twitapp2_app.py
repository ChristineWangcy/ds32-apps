'''app for twit'''
import os
from flask import Flask, render_template, request
from .models import DB, User, Tweet

from .twitter import get_user_and_tweets
from .predict import predict_user


def create_app():
    # initializes our app
    app = Flask(__name__)

    file_path = os.path.join(app.root_path, 'db.sqlite3')
    # Database configurations
    # app.config["SQLALCHEMY_DATA_URI"] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Give our APP access to our database
    DB.init_app(app)
    with app.app_context():
        DB.create_all()

    # Listen to a "route"
    # '/' is the home page route
    @app.route('/')
    def root():
        # query the DB for all users
        users = User.query.all()
        # what I want to happen when somebody goes to home page
        return render_template('base.html', title="Home", users=users)

    # kind of like what Jinja2 does to our web pages
    app_title = 'Twitoff DS32'

    @app.route('/add_user', methods=['POST'])
    def add_user():
        user = request.form.get('user_name')
        try:
            response = get_user_and_tweets(user)
            if not response:
                return 'Nothing was added.' \
                       '<br><br><a href="/" class="button warning">Go Back!</a>'
            else:
                return f'User: {user} successfully added!' \
                       '<br><br><a href="/" class="button warning">Go Back!</a>'
        except Exception as e:
            return str(e)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # request.values is pulling data from the html
        # use the username from the URL (route)
        # or grab it from the dropdown menu
        name = name or request.values['user_name']

        # If the user exists in the db already, update it, and query for it

        try:
            if request.method == 'POST':
                user = request.form.get('user_name')
                try:
                    response = get_user_and_tweets(user)
                    if not response:
                        return 'Nothing was added.' \
                            '<br><br><a href="/" class="button warning">Go Back!</a>'
                    else:
                        return f'User: {user} successfully added!' \
                            '<br><br><a href="/" class="button warning">Go Back!</a>'
                except Exception as e:
                    return str(e)

            # From the user that was just added / Updated
            # get their tweets to display on the /user/<name> page
            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def predict():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            if prediction == 0:
                predicted_user = user0
                non_predicted_user = user1
            else:
                predicted_user = user1
                non_predicted_user = user0
            message = f"'{request.values['tweet_text']}' is more likely to be said by '{predicted_user}' than by '{non_predicted_user}'"

        return render_template('predict.html', title='Prediction', message=message)

    @ app.route('/reset')
    def reset():
        # remove everything from the database
        DB.drop_all()
        # Creates the database file initially.
        DB.create_all()
        return "reset"

    return app


if __name__ == '__main__':
    create_app().run()
