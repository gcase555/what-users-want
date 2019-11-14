import os

import flask_admin as admin
from flask import Flask
from flask_cors import CORS
from flask_security import Security, login_required, http_auth_required
from werkzeug.utils import redirect

import models
from models import ModelView

DEBUG = os.environ['FLASK_DEBUG']
HOST = '0.0.0.0'
PORT = 8001

app = Flask(__name__)
# TODO: Set this in prod before deploying
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']
#app.register_blueprint(content_api, url_prefix='/api/v1')
#app.register_blueprint(tweet_api, url_prefix='/api/v1')
# TODO: Set this in prod before deploying
app.config['SECURITY_PASSWORD_SALT'] = os.environ['DB_SALT']
#TODO: FIXME with CORS
cors = CORS(app, resources={r"/INSERT_SOME_ROUTE/*": {"origins": "*"}})
security = Security(app, models.user_datastore)

#TODO: FIXME add models here
admin = admin.Admin(app, name='feature-dashboard', index_view=models.MyAdminIndex())
admin.add_view(ModelView(models.Tag))


@app.before_request
def initialize():
    models.initialize()


@app.after_request
def after_request(response):
    models.clean_up()
    return response  

@app.route('/health')
def health_check():
    return 'OK'


@login_required
@app.route('/login')
def login():
    return redirect('/admin')

@app.route('/')
@login_required
def welcome():
    return 'Welcome!'

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
