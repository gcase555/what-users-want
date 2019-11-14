import datetime
import os
import urllib.parse

from flask_admin import AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from flask_security import Security, PeeweeUserDatastore, \
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
    user = ForeignKeyField(User, related_name='user-meta')
    profession = TextField(null=True)
    age = IntegerField(null=True)
    country = CharField(null=True)
    city = CharField(null=True)
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

class ProductQuestionare(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    score = DecimalField()

class ProductQuestion(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    questionare = ForeignKeyField(ProductQuestionare)
    question = CharField()
    text_answer = TextField(null=True)
    num_answer = DecimalField(null=True)

class UserProductSentiment(BaseModel):
    user = ForeignKeyField(User, related_name='product')
    product = ForeignKeyField(User, related_name='user')
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.datetime.now, index=True)
    score = DecimalField()


class Feature(BaseModel):
    product = ForeignKeyField(Product, related_name='feature')
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.datetime.now, index=True)
    name = CharField()
    status = CharField(null=True)
    publish = BooleanField(default=True)
    description = TextField(null=True)    
    current_score = DecimalField(null=True)

class Tag(BaseModel):
    name = CharField()

class FeatureTags(BaseModel):
    feature = ForeignKeyField(Feature, related_name='tags')
    tag = ForeignKeyField(Tag, related_name='features')
    name = property(lambda self: self.tag.name)

class UserFeatureVote(BaseModel):
    user = ForeignKeyField(User, related_name='feature-points')
    product = ForeignKeyField(Product, related_name='feature-points')
    feature = ForeignKeyField(Feature, related_name='feature-points')
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.datetime.now, index=True)
    user_voted = property(lambda self: self.user.email)
    product_voted = property(lambda self: self.product.name)
    feature_voted = property(lambda self: self.feature.name)
    vote_points = IntegerField(index=True)
    comment = CharField(max_length=300)
    publish = BooleanField()

class UserProductVoteScores(BaseModel):
    user = ForeignKeyField(User, related_name='user-product-points')
    product = ForeignKeyField(Product, related_name='user-product-points')
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.datetime.now, index=True)
    user_voted = property(lambda self: self.user.email)
    product_voted = property(lambda self: self.product.name)
    current_score = DecimalField(null=True)
    max_score = property(lambda self: self.product.max_user_votes_total)

class ModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


user_datastore = PeeweeUserDatastore(DATABASE, User, Role, UserRoles)

def initialize():
    # DATABASE.get_conn()
    DATABASE.create_tables([User, Role, UserRoles, UserProductVoteScores, FeatureTags, Tag, Feature, UserProductSentiment, Product, ProductQuestionare, ProductQuestion], safe=True)
    # # Switch this line out for create_tables in order to do a database migration,
    # # set interactive to TRUE only once you have verified the change wont break prod
    #DATABASE.evolve(interactive=False)
    # DATABASE.close()
def clean_up():
    DATABASE.close()
