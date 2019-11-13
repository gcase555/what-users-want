from flask_security import utils

from main import app
from models import user_datastore, DATABASE
import os

try:
    DATABASE.connect()
    with app.app_context():
        admin_username = 'team-admin@dev.null'
        product_admin_username = 'product-admin@dev.null'
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='product-admin', description='CRUD role for product data')
        if not user_datastore.get_user(admin_username):
            admin_hashed = utils.hash_password(os.environ['ADMIN_KEY'])
            user_datastore.create_user(email=admin_username, password=admin_hashed)
        if not user_datastore.get_user(product_admin_username):
            pm_admin_hashed = utils.hash_password(os.environ['PM_ADMIN_KEY'])
            user_datastore.create_user(email=product_admin_username, password=pm_admin_hashed)
        user_datastore.add_role_to_user(admin_username, 'admin')
        user_datastore.add_role_to_user(product_admin_username, 'product-admin')
        DATABASE.close()
        print('Successfully created service users')
except SystemError as E:
    print('Users already created:', E)
