import os
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from PIL import Image
import matplotlib.pyplot as mat
import numpy as np

def reshape_all_the_images_to_fixed_size(total_number_of_images, fixed_shape):
    for i,x in enumerate(total_number_of_images):
        if total_number_of_images[i].shape != fixed_shape:
            total_number_of_images[i] = (total_number_of_images[i][:,:,0:-1])
    return np.array(total_number_of_images)

def compute_value_counts(labels_associated_with_the_images):
    count_values = {}
    for x in labels_associated_with_the_images:
        if x not in count_values:
            count_values[x] = 0
        else:
            count_values[x] = count_values[x] + 1
    for x in count_values.keys():
        print("the number of points available in the domain", x, count_values[x])
    return count_values

#create dataset 
fixed_shape = (300, 300, 3)
total_number_of_images = []
labels_associated_with_the_images = []
root_image_path = 'drive/My Drive/Classroom/images/'
for domain in [x for x in os.listdir(root_image_path) if x!='.DS_Store']:
    for y in [x for x in os.listdir(root_image_path+domain) if x!='.DS_Store']:
        total_number_of_images.append((f"{root_image_path}{domain}/{y}"))
        labels_associated_with_the_images.append(domain)
total_number_of_images = np.array(total_number_of_images)

def generator(batch_size, fixed_shape):
    selected_batch = []
    np.random.shuffle(total_number_of_images)
    for url in total_number_of_images[:batch_size]:
        selected_batch.append(np.array(Image.open(url).resize(fixed_shape[0:2], Image.ANTIALIAS))/255.0)
    return reshape_all_the_images_to_fixed_size(selected_batch, fixed_shape)



print("model initialization begins")
K.clear_session()

input_img = Input(shape=(300, 300, 3)) # 1ch=black&white, 28 x 28
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(input_img) #nb_filter, nb_row, nb_col
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
encoded = MaxPooling2D((2, 2), border_mode='same')(x)

print ("shape of encoded", K.int_shape(encoded))

x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = UpSampling2D((2, 2))(x)

x = Convolution2D(16, 3, 3, activation='relu', border_mode='valid')(x) 

x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(3, 5, 5, activation='sigmoid', border_mode='same')(x)
print ("shape of decoded", K.int_shape(decoded))

autoencoder = Model(input_img, decoded)
encoder = Model(inputs=input_img, outputs=encoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')


from keras.callbacks import TensorBoard

for i in range(10000):
    x_train = generator(100, fixed_shape)
    x_test = generator(100, fixed_shape)

    
    autoencoder.fit(x_train_noisy, x_train, nb_epoch=1, batch_size=25,
               shuffle=True, validation_data=(x_test_noisy, x_test), verbose=1)
    autoencoder.save('save/model'+str(i)+'.h5')
    encoder.save('save/model_encoder'+ str(i)+'.h5')
    print("Saved model to disk epoch number ", str(i))