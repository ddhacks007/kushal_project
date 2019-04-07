# importing packages
import operations_common
import tf_model
from tensorflow.core.protobuf import saver_pb2
import numpy as np
from PIL import Image
import tensorflow as tf
import os
import sys
sys.path.append("..")

# generate images according to the batch size on given image urls
def generator(batch_size, fixed_shape, total_image_paths):
    selected_batch = []
    np.random.shuffle(total_image_paths)
    for url in total_image_paths[:batch_size]:
        selected_batch.append(np.array(Image.open(url).resize(
            fixed_shape[0:2], Image.ANTIALIAS))/255.0)
    return operations_common.reshape_all_the_images_to_fixed_size(selected_batch, fixed_shape)


# it will start the training process for our model
def begin_training(total_image_paths, learning_rate=0.001, epochs=10000000, batch_size=100,  noise_factor=0.1, loc=0.0, scale=1.0):
    operations_common.ensure_dir('save/')
    cross_entropy = -1. * tf_model.targets_ * \
        tf.log(tf_model.logits) - (1. - tf_model.targets_) * \
        tf.log(1. - tf_model.logits)
    cost = tf.reduce_mean(cross_entropy)
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    check = tf.add_check_numerics_ops()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver(write_version=saver_pb2.SaverDef.V2)
    for e in range(epochs):
        print("epoch number", e)
        for images in range(len(total_image_paths)-batch_size):
            imgs = generator(batch_size, fixed_shape, total_image_paths)
            img_noise = imgs + noise_factor * \
                np.random.normal(loc=loc, scale=scale, size=imgs.shape)
            batch_cost, _ = sess.run([cost, optimizer], feed_dict={
                                     tf_model.inputs_: img_noise, tf_model.targets_: imgs})
            save_path = saver.save(sess, "save/jewellery_model.ckpt")
            print("Epoch: {}/{}...".format(e+1, epochs),
                  "Training loss: {:.4f}".format(batch_cost))


if __name__ == "__main__":
    fixed_shape = (230, 230, 3)
    root_image_path = '../../images/'
    total_image_paths = operations_common.get_images(
        fixed_shape, root_image_path, specification='path')
    begin_training(total_image_paths)