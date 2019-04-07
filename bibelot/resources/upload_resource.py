import os
import numpy as np
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask import Flask, flash, request
import json
from PIL import Image
from datetime import datetime
from models import Upload
import requests

class UploadResource(Resource):
  def __init__(self):
      pass

  def get(self, image_url):
    try:
      image_url = '/'.join(image_url.split('@'))
      image_requested = Image.open(requests.get(image_url, stream = True).raw)
      filename = os.environ['SOURCE_IMG']
      tmp_location = self.get_temp_location()
      location = os.path.join(tmp_location, filename)
      image_requested.save(location)
      os.system("bash span_worker.sh")
      return json.dumps({'recommendations_url': [np.load('../sparkler/recommendations_paths.npy').item()]})
    except: 
      return json.dumps({'recommendations_url': 'failed'})

  def get_temp_location(self):
    location = os.path.join(os.environ['GET_SOURCE_DIR'])
    if not os.path.isdir(location):
      os.makedirs(location)
    else:
      _ = [os.remove(os.path.join(location,i)) for i in os.listdir(location)]
    return location

  def save_to_tmp(self):
    file = request.files['file']
    filename = os.environ['SOURCE_IMG']
    print(filename)
    tmp_location = self.get_temp_location()
    location = os.path.join(tmp_location, filename)
    file.save(location)
    return location,filename
  
  def save_meta(self, shop_name, file_date, type_of_file):
    try:
      upload = Upload().create(shop_name, file_date, type_of_file)
      return True
    except:
      return False

  def post(self):
    shop_name = request.form['shop_name']
    type_of_file = request.form['file_type']
    print(shop_name, type_of_file)
    file_date = datetime.date(datetime.now())
    location, filename = self.save_to_tmp()
    print(f"Upload to {location} complete")
    if self.save_meta(shop_name, file_date, type_of_file) == True:
      os.system("bash span_worker.sh")
      return json.dumps({'recommendations_url': [np.load('../sparkler/recommendations_paths.npy').item()]})
    return json.dumps({'recommendations_url': 'failed'})