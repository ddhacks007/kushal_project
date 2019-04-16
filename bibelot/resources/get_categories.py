from flask import Flask
import os
from flask_restful import Resource
import numpy as np
import json
import sys
import sys
sys.path.append('../operations_common/')
import operations_common

class GetCategories(Resource):
    def get(self):
        return json.dumps({"list_of_categories":[ x.split('/')[1] for x in operations_common.list_all_sub_folders_s3('images/', 'kushal-jewels')]})
