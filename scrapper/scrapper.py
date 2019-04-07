#importing libraries
import requests 
from bs4 import BeautifulSoup 
import numpy as np
import urllib.request
import os
import pandas as pd
import time
import sys
sys.path.append('../operations_common/')
import operations_common
from PIL import Image

#it contains the textual information and url for the photos for all the products
dict_of_information_of_jewellerys = {}
#it contains the url for failed to scrap products
scrapper_failed_list_of_jewellerys = []
#flattens 2d list to single numpy array
def convert_2d_list_to_numpy(two_d_list):
    flatten_list = []
    for x in (two_d_list):
        for y in x:
            flatten_list.append(y)
    return np.array(flatten_list)

#fetches the number of domains available in the site
def get_me_the_list_of_titles(URL = "https://www.kushals.com/collections/"):
    print('scrapping started !!')
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    x = str(soup).replace('\n', '').split('<a href="/collections/')[1:]
    return [x.split('>')[1].split('<')[0].lower().replace(' ','-') if x.split('>')[1].split('<')[0].lower().replace(' ','-') != 'bangles-and-bracelets' else 'bangles-bracelets-kadas' for x in [i  for i in x if 'title' in i][1:6]]

#ensures the requested file path exists if not will create a file path
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

#scraps the url for the images
def scrap_list_of_images_url(list_of_scrapped):
    list_of_images = []
    for i,x in enumerate(list_of_scrapped[:-1]):
        if i==0:
            list_of_images.append(x.split('property="og:image"/>')[0].split('<meta content=')[-1][8:].replace('"', '').replace(' ', ''))
        else:
            list_of_images.append(x.split('<meta content=')[-1][8:].replace('"', '').replace(' ',''))
    return list_of_images

#scraps the content for each product in the website
def get_me_the_contents(sub_url):
    try:
        print('scrapping the contents for sub_url ', sub_url)
        entire_information_about_product = {}
        URL = "https://www.kushals.com"+sub_url
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html5lib')
        table_of_info_about_jewel = str(soup).replace('\n', '').split('<tr id="KushTable">')[1].split('<div class="desc">')[0].split('<th scope="row"')[1:]
        for x in table_of_info_about_jewel:
            entire_information_about_product[x.split('</th>')[0][1:].replace('.', '').replace(' ', '').replace('-', '')] = x.split('<td>')[1].split('</td>')[0]
        entire_information_about_product['image_urls'] = scrap_list_of_images_url(str(soup).split('property="og:image"/>'))
        return entire_information_about_product
    except:
        scrapper_failed_list_of_jewellerys.append(sub_url)
        
#heart of the program here is where the scrap for the particular domain begins
def begin_to_scrap_the_urls(jewel_domain):
    global dict_of_information_of_jewellerys
    dict_of_information_of_jewellerys[jewel_domain] = []
    pages = 1
    collection_of_urls = []
    while True:
        print ('scrapping the '+jewel_domain+' at page_no ',pages)
        URL = 'https://www.kushals.com/collections/'+jewel_domain+'?page='+str(pages)
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html5lib')
        list_of_images_urls = []
        list_of_images = str(soup).replace('\n', "").split('<div class="prod-image">')
        for x in range(1, len(list_of_images)):
            list_of_images_urls.append(list_of_images[x].split('<a href=')[1].split('title')[0])
        if list_of_images_urls == []:
            break
        else:
            collection_of_urls.append(list_of_images_urls)
            pages = pages + 1
            list_of_images_urls = []
    collection_of_urls = convert_2d_list_to_numpy(collection_of_urls)
    for url in (collection_of_urls):
        dict_of_information_of_jewellerys[jewel_domain].append(get_me_the_contents(url.replace('"', '').replace(' ', '')))
        


#download the images from the url requested and store it inside the predefined location
def upload_images_to_s3(domain, list_available_in_domain):
    store_root_dir = 'images/'+domain+'/'
    global_number = 0
    try:
        for item_details in list_available_in_domain:
            for image_url in item_details['image_urls']:
                store_dir = store_root_dir+str(global_number)+'.jpeg'
                image = Image.open(requests.get('https://'+image_url, stream = True).raw).resize((230, 230), Image.ANTIALIAS)
                shape = np.array(image).shape
                if  shape != (230, 230, 3):
                      image = Image.fromarray(operations_common.reshape_all_the_images_to_fixed_size([np.array(image)], (230, 230, 3))[0])
                operations_common.upload_s3(store_dir, image, 'kushal-jewels')
                global_number = global_number + 1
    except:
        for image_url in item_details['image_urls']:
            store_dir = store_root_dir+str(global_number)+'.jpeg'
            image = Image.open(requests.get('https://'+image_url, stream = True).raw).resize((230, 230), Image.ANTIALIAS)
            shape = np.array(image).shape
            if shape != (230, 230, 3):
                      image = Image.fromarray(operations_common.reshape_all_the_images_to_fixed_size([np.array(image)], (230, 230, 3))[0])
            operations_common.upload_s3(store_dir, image, 'kushal-jewels')
            global_number = global_number + 1


#download images for all the domains one by one and upload to s3 bucket
def download_upload():
    print('download and upload is initiated!!')
    for i in dict_of_information_of_jewellerys.keys():
        upload_images_to_s3(i, [x  for x in dict_of_information_of_jewellerys[i] if x!=None ])
    
#this is the start of the program to initiate scrapping
def execute():
    for jewel_domain in get_me_the_list_of_titles():
        print('scrapping for the jewel with the domain ', jewel_domain, '!!')
        begin_to_scrap_the_urls(jewel_domain)

if __name__ == '__main__':
    start = time.time()
    execute()
    download_upload()
    print('time taken to complete the upload to s3', time.time() - start)