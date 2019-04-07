import os
import tensorflow as tf
from PIL import Image
import numpy as np
from tensorflow.core.protobuf import saver_pb2
from recommendation_trainer import tf_model
import matplotlib.pyplot as mat
import functools
import time
import tables


#gives the encoder dimmensionality
def get_encoder_dimmensions():
        return functools.reduce((lambda x,y:x*y), [int(x) for x in tf_model.encoded.shape[1:]])

#reshapes all the images according to the fixed_size specified
def reshape_all_the_images_to_fixed_size(total_number_of_images, fixed_shape):
    for i, x in enumerate(total_number_of_images):
        if total_number_of_images[i].shape != fixed_shape:
            total_number_of_images[i] = (total_number_of_images[i][:, :, 0:-1])
    return np.array(total_number_of_images)

#gives the encoded vector for the images
def calculate_encoded_vectors_for_images(fixed_shape):
    saver = tf.train.Saver(write_version = saver_pb2.SaverDef.V2)
    with tf.Session() as sess:
    # Restore variables from disk.
        saver.restore(sess, "recommendation_trainer/save/jewellery_model.ckpt")
        with tables.open_file('total_images_encoded.tbl', 'r') as h5_file:
            total_images_encoded = h5_file.root.total_images_encoded.read()
        source_image_encoded = sess.run(tf_model.encoded, feed_dict = {tf_model.inputs_: reshape_all_the_images_to_fixed_size([np.array(Image.open('source/source.jpeg').resize((230, 230), Image.ANTIALIAS))], fixed_shape)/255.0}).reshape(1,get_encoder_dimmensions())
    return (total_images_encoded, source_image_encoded)

#finding the  neigbours which has semantics similar to the image  
def calculate_nearest_neighbours_with_the_images(total_images_encoded, source_image_encoded, threshold):
    return np.argsort(np.sqrt((np.array(total_images_encoded)- np.array(source_image_encoded.flatten()))**2).sum(axis = 1))[:threshold]

#spans the recommendation after the images are loaded
def span_the_recommendation(fixed_shape, full_paths_urls, threshold):
    start = time.time()
    total_images_encoded, source_image_encoded = calculate_encoded_vectors_for_images(fixed_shape)             
    min_dist_of_images = calculate_nearest_neighbours_with_the_images(total_images_encoded, source_image_encoded, threshold=threshold)
    print('time taken to calculate_nearest_neighbours', time.time() - start)
    return full_paths_urls[min_dist_of_images]

def convert_to_relevant_form_save(recommendation_s3_paths):
        dict_paths = {}
        for path in recommendation_s3_paths:
            key = path.split('/')[1]
            if key not in dict_paths.keys():
                dict_paths[key] = []
                dict_paths[key].append(path)
            else:
                dict_paths[key].append(path)
        np.save('recommendations_paths.npy', dict_paths)

if __name__ == "__main__":
    start = time.time()
    os.system('rm recommendations_paths.npy')
    fixed_shape = (230, 230, 3)
    threshold = 30
    full_paths_urls = np.load('full_paths_url.txt')
    recommendations_s3_paths = span_the_recommendation(fixed_shape, full_paths_urls, threshold)
    print('total time taken to execute the entire script', time.time() - start)
    convert_to_relevant_form_save(recommendations_s3_paths)
    print('time taken to execute the entire runner', time.time() - start)