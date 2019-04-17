from flask import Flask
import os
from flask_restful import Resource
import numpy as np
import json
import sys
import sys
sys.path.append('../operations_common/')
import operations_common

class GetImageUrlsPages(Resource):
    def get(self, category_name, page_number):
        urls_pages = operations_common.get_image_urls_with_page(category_name, int(page_number))
        return json.dumps({"image_urls": urls_pages[0], "pages":int(urls_pages[1]/50)})
