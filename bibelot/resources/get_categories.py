from flask import Flask
import os
from flask_restful import Resource
import numpy as np
import json

class GetCategories(Resource):
    def get(self):
        return json.dumps({"list_of_categories":list(np.load('../meta_info_jewels.txt'))})
