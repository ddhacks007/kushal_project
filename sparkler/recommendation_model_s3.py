#importing libraries
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from tensorflow.core.protobuf import saver_pb2
from recommendation_trainer import tf_model
import matplotlib.pyplot as mat
import sys
sys.path.append('../operations_common/')
import operations_common
import functools
import requests
import io

#giving ranking to each image belonging to particular category
def assign_numbers_to_images_in_dir(obtained_directory):
        return len(os.listdir(obtained_directory))

#gives the encoder dimmensionality
def get_encoder_dimmensions():
        return functools.reduce((lambda x,y:x*y), [int(x) for x in tf_model.encoded.shape[1:]])

#gives the encoded vector for the images
def calculate_encoded_vectors_for_images(fixed_shape, image_urls):
    saver = tf.train.Saver(write_version = saver_pb2.SaverDef.V2)
    with tf.Session() as sess:
    # Restore variables from disk.
        distance_vector = []
        saver.restore(sess, "recommendation_trainer/save/jewellery_model.ckpt")
        for i in range(len(image_urls)):
            print(i)
            k = requests.get('https://s3.ap-south-1.amazonaws.com/kushal-jewels/'+image_urls[i])
            image = operations_common.reshape_all_the_images_to_fixed_size([np.array(Image.open(io.BytesIO(k.content)).resize(fixed_shape[0:2], Image.ANTIALIAS))/255.0], fixed_shape)
            image_encoded = sess.run(tf_model.encoded, feed_dict ={tf_model.inputs_: image.reshape(tuple([1]+list(fixed_shape)))})
            image_encoded = np.array(image_encoded).reshape(1, get_encoder_dimmensions())
            source_image_encoded = sess.run(tf_model.encoded, feed_dict = {tf_model.inputs_: operations_common.reshape_all_the_images_to_fixed_size([np.array(Image.open('source/source.jpeg').resize((230, 230), Image.ANTIALIAS))], fixed_shape)/255.0}).reshape(1,get_encoder_dimmensions())
            distance_vector.append(calculate_nearest_neighbours_with_the_images(image_encoded, source_image_encoded)[0])
    return np.array(distance_vector)

#finding the  neigbours which has semantics similar to the image  
def calculate_nearest_neighbours_with_the_images(total_images_encoded, source_image_encoded):
    return np.sqrt((np.array(total_images_encoded)- np.array(source_image_encoded.flatten()))**2).sum(axis = 1)
#spans the recommendation after the images are loaded
def span_the_recommendation(fixed_shape, image_urls, threshold):
    distance_vector = calculate_encoded_vectors_for_images(fixed_shape, image_urls)             
    image_urls = np.array(image_urls)[np.argsort(distance_vector)][:threshold]
    counter = 0
    for i, j in enumerate(image_urls):
        directory_save = '../recommendations/'+j.split('/')[1]
        operations_common.ensure_dir(directory_save+'/')
        k = requests.get('https://s3.ap-south-1.amazonaws.com/kushal-jewels/'+j)
        image = operations_common.reshape_all_the_images_to_fixed_size([np.array(Image.open(io.BytesIO(k.content)).resize(fixed_shape[0:2], Image.ANTIALIAS))/255.0], fixed_shape)
        mat.imsave(f"{directory_save}/image_number{(assign_numbers_to_images_in_dir(directory_save))+1}.jpeg", image[0])
            
if __name__ == "__main__":
    fixed_shape = (230, 230, 3)
    threshold = 30
    image_urls = operations_common.list_all_image_urls_s3('images/','kushal-jewels')
    span_the_recommendation(fixed_shape, image_urls[:100], threshold = threshold)