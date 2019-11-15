from datetime import datetime, timedelta

from flask import Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields,
                               marshal, marshal_with)
from flask_security import http_auth_required, roles_accepted
from peewee import IntegrityError, DoesNotExist

from models import Feature, DATABASE

feature_fields = {
    'product': fields.String,
    'name': fields.String,
    'description': fields.String
}

def feature_or_404(id):
    try:
        print("getting id ", id)
        feature = Feature.get(Feature.id == id)
    except DoesNotExist:
        abort(404)
    else:
        return feature

class FeatureRoutes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'product',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'name',
            required=True,
            location=['form', 'json']
        )
        super().__init__()
    
    @marshal_with(feature_fields)
    def get(self, id):
        return feature_or_404(id)
    
    @marshal_with(feature_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print('feature to be created: {}'.format(args.product))
        with DATABASE.atomic():
            # TODO get product ID Here
            feature = Feature.create(**args)
        return feature, 201

feature_api = Blueprint('resources.features', __name__)


api = Api(feature_api)
# api.add_resource(
#     Feature,
#     '/feature',
#     endpoint='features'
# )
api.add_resource(
    FeatureRoutes,
    '/features/<int:id>',
    endpoint='feature'
)

api.add_resource(
    FeatureRoutes,
    '/feature',
    endpoint='feature-post'
)