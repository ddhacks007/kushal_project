from flask import Flask
import os
from flask_cors import CORS
from resources.upload_resource import UploadResource
from config import Config
from resources.get_categories import GetCategories
from flask_sqlalchemy import SQLAlchemy
from database import init_db

def initiate_app(app):
    upload_view = UploadResource.as_view('upload_view')
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.add_url_rule('/upload', view_func=upload_view, methods=['POST'])
    app.add_url_rule('/retrieve/<image_url>', view_func=upload_view, methods = ['GET'])
    get_categories_view = GetCategories.as_view('get_categories_view')
    app.add_url_rule('/categories', view_func=get_categories_view, methods = ['GET'])
    CORS(app)
    return app

def create_app():
   return initiate_app(Flask(__name__))

app = create_app()
init_db()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
    init_db()