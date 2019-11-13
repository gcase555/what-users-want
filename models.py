import datetime
import os
import urllib.parse
# import peeweedbevolve

from flask_admin import AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from flask_security import PeeweeUserDatastore, \
    UserMixin, RoleMixin
from peewee import *

# parameters for postgres connection http://initd.org/psycopg/docs/module.html#psycopg2.connect
# http://docs.peewee-orm.com/en/latest/peewee/database.html

if 'DATABASE_URL' in os.environ:
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
    DATABASE = PostgresqlDatabase(
        'ss_db',
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        autocommit=True,
        autorollback=True
    )
else:
    DATABASE = PostgresqlDatabase(
        'ssdb',
        user='vagrant',
        password='vagrant',
        host='localhost',
        port=15432,
        autocommit=True,
        autorollback=True
    )


class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(BaseModel, UserMixin):
    email = CharField(unique=True, index=True)
    password = CharField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

class UserMeta(BaseModel):
    user = ForeignKeyField(User, backref='user-meta')
    profession = TextField(null=True)
    age = IntegerField(null=True)
    country = CharField()
    city = CharField()
    state = CharField(null=True)

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)


class Product(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)
    max_sentiment_total = IntegerField(default=50)
    max_user_votes_total = IntegerField(default=40)

class UserProductSentiment(BaseModel):
    user = ForeignKeyField(User, related_name='product')
    product = ForeignKeyField(User, related_name='user')
    created_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    total = IntegerField()


class Feature(BaseModel):
    product = ForeignKeyField(Product, backref='feature')
    created_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    name = CharField()
    description = TextField(null=True)    
    current_score = IntegerField(null=True)

class Tag(BaseModel)
    name = CharField()

class FeatureTags(BaseModel)
    feature = ForeignKeyField(Feature, related_name='tags')
    tag = ForeignKeyField(Tag, related_name='features')
    name = property(lambda self: self.tag.name)

class UserFeatureVotes(BaseModel):
    user = ForeignKeyField(User, backref='feature-points')
    product = ForeignKeyField(Product, backref='feature-points')
    feature = ForeignKeyField(Feature, backref='feature-points')
    created_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    user_voted = property(lambda self: self.user.email)
    product_voted = property(lambda self: self.product.name)
    feature_voted = property(lambda self: self.feature.name)
    vote_points = IntegerField(index=True)
    text = CharField(max_length=300)

class UserProductVoteScores(BaseModel):
    user = ForeignKeyField(User, backref='user-product-points')
    product = ForeignKeyField(Product, backref='user-product-points')
    created_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    user_voted = property(lambda self: self.user.email)
    product_voted = property(lambda self: self.product.name)
    current_score = IntegerField()
    max_score = property(lambda self: self.product.max_user_votes_total)

class ModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')


user_datastore = PeeweeUserDatastore(DATABASE, User, Role, UserRoles)

def initialize():
    DATABASE.get_conn()
    DATABASE.create_tables([User, Role, UserRoles, UserProductVoteScores, FeatureTags, Tag, Feature, UserProductSentiment, Product], safe=True)
    # # Switch this line out for create_tables in order to do a database migration,
    # # set interactive to TRUE only once you have verified the change wont break prod
    # # DATABASE.evolve(interactive=False)
    # DATABASE.close()
def clean_up():
    DATABASE.close()
