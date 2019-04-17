#importing libraries
import os
import numpy as np
from PIL import Image
import boto3
from boto.s3.connection import S3Connection
import math 

#removes the .ds_store which comes when computing list of dirs in the directories
def removeds_store(path_of_directory):
    return [x for x in os.listdir(path_of_directory) if x!='.DS_Store']

#reshapes all the images according to the fixed_size specified
def reshape_all_the_images_to_fixed_size(total_number_of_images, fixed_shape):
    for i, x in enumerate(total_number_of_images):
        if total_number_of_images[i].shape != fixed_shape:
            total_number_of_images[i] = (total_number_of_images[i][:, :, 0:-1])
    return np.array(total_number_of_images)

#get array of images and append it to the list
def get_image_vectors(fixed_shape, root_image_path):
    total_number_of_images = []
    labels_associated_with_the_images = [] 
    for domain in removeds_store(root_image_path):
        for y in removeds_store(root_image_path+domain):
            total_number_of_images.append(np.array(Image.open(f"{root_image_path}{domain}/{y}").resize(fixed_shape[0:2], Image.ANTIALIAS))/255.0)
            labels_associated_with_the_images.append('images'+(root_image_path+domain+'/'+y).split('images')[1])
    return (reshape_all_the_images_to_fixed_size(total_number_of_images, fixed_shape), np.array(labels_associated_with_the_images))

#get_image_details_according_to_the_specification
def get_images(fixed_shape, root_image_path):
        return get_image_vectors(fixed_shape, root_image_path)

#computed value counts for all images so that we can check imbalancy in future
def compute_value_counts(labels_associated_with_the_images):
    count_values = {}
    for x in labels_associated_with_the_images:
        if x not in count_values:
            count_values[x] = 0
        else:
            count_values[x] = count_values[x] + 1
    for x in count_values.keys():
        print("the number of points available in the domain",
              x, count_values[x])
    return count_values

#ensures whether directory exists if not creates it
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  

#initial bucket connection
def init_bucket_s3_connection(bucket_name):
    try:
        conn = S3Connection('AKIAQNL5LVB3ZWB3MQC3', 'iYe7KwyydUeWDr9SW1jnbPCJdbIhX3A23sCO24Ri', host= 's3.ap-south-1.amazonaws.com')
        bucket = conn.get_bucket(bucket_name)
        return bucket
    except:
        return False

#delete bucket files
def delete_files_bucket(folder_name, bucket_name):
    try:
        bucket = init_bucket_s3_connection(bucket_name)
        for key in bucket.list(prefix = folder_name+'/'):
            key.delete()
        return True
    except:
        return False

#initial connection resource
def init_connection_resource(bucket_name):
    try:
        return  boto3.resource(
        's3',
        aws_access_key_id='AKIAQNL5LVB3ZWB3MQC3',
        aws_secret_access_key='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',
        ).Bucket(bucket_name)
    except:
        return False

#inorder to upload files to the s3
def upload_s3(file_path, image, bucket_name):
    image.save('temp.jpeg')
    init_connection_resource(bucket_name).put_object(Key=file_path, Body=open('temp.jpeg', 'rb').read(), ACL='public-read')

#sub_folders list from the root folder
def list_all_image_urls_s3(image_file, bucket_name):
    bucket = init_bucket_s3_connection(bucket_name)
    image_urls = []
    for sub_folders in  bucket.list(prefix = image_file, delimiter = '/'):
        for image_files in bucket.list(prefix = sub_folders.name, delimiter = '/'):
            image_urls.append(image_files.name)
    return image_urls

#get_file_paths_in_s3_bucket
def number_of_files_present_in_path_s3(directory_path, bucket_name):
    bucket = init_bucket_s3_connection(bucket_name)
    counter = 0
    for sub_folders in bucket.list(prefix = directory_path, delimiter = '/'):
        counter = counter + 1
    return counter

def list_all_sub_folders_s3(url_path, bucket_name):
    bucket = init_bucket_s3_connection(bucket_name)
    sub_folders_names = []
    for sub_folders in  bucket.list(prefix = url_path, delimiter = '/'):
        sub_folders_names.append(sub_folders.name)
    return sub_folders_names

def round_it_to_near(number_obtained, round_number):
    while True:
        if number_obtained%round_number == 0:
            return number_obtained
        else:
            number_obtained = number_obtained + 1


def get_image_urls_with_page(category_name, page):
    init_page = (page-1)*50
    pages = init_page + 50
    fetch_url = 'https://s3.ap-south-1.amazonaws.com/kushal-jewels/images/'
    total_number_of_images_available = number_of_files_present_in_path_s3(os.path.join('images/',category_name+'/'), 'kushal-jewels')
    os.path.join(fetch_url, category_name)
    if((total_number_of_images_available - init_page)>=50):
        return ([fetch_url+category_name+'/'+str(x)+'.jpeg' for x in range(init_page, pages)], round_it_to_near(total_number_of_images_available, 50))
    else:
        return ([fetch_url+category_name+'/'+str(x)+'.jpeg' for x in range(init_page,   total_number_of_images_available)], round_it_to_near(total_number_of_images_available, 50))
    