import os

import flask_admin as admin
from flask import Flask
from flask_cors import CORS
from flask_security import Security, login_required, http_auth_required
from werkzeug.utils import redirect

import models
from models import ModelView
from resources.features import feature_api

DEBUG = os.environ['FLASK_DEBUG']
HOST = '0.0.0.0'
PORT = 8001

app = Flask(__name__)
# TODO: Set this in prod before deploying
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']
app.register_blueprint(feature_api, url_prefix='/api/v1')
# TODO: Set this in prod before deploying
app.config['SECURITY_PASSWORD_SALT'] = os.environ['DB_SALT']
#TODO: FIXME with CORS
cors = CORS(app, resources={r"/INSERT_SOME_ROUTE/*": {"origins": "*"}})
security = Security(app, models.user_datastore)

#TODO: FIXME add models here
admin = admin.Admin(app, name='Feature Pulse', index_view=models.MyAdminIndex())
admin.add_view(models.UserFeatureVoteModelView(models.UserFeatureVote, category="Feature"))
admin.add_view(models.FeatureModelView(models.Feature, category="Feature"))
admin.add_view(ModelView(models.Tag, category="Tags"))
admin.add_view(ModelView(models.FeatureTags, category="Tags"))
admin.add_view(ModelView(models.Product, category="Product"))
admin.add_view(ModelView(models.UserProductSentiment, category="Product"))
admin.add_view(ModelView(models.UserProductVoteScores, category="Product"))
admin.add_view(ModelView(models.UserMeta, category="User"))


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
def welcome():
    return 'Welcome!'

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
