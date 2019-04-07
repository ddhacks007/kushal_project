import tensorflow as tf

tf.reset_default_graph()
inputs_ = tf.placeholder(tf.float32, (None, 230, 230, 3), name='inputs')
targets_ = tf.placeholder(tf.float32, (None, 230, 230, 3), name='targets')


conv1 = tf.layers.conv2d(inputs_, 32, kernel_size=(3, 3), padding='same', activation=tf.nn.relu)
conv1 = tf.layers.batch_normalization(conv1, axis=3)
maxpool1 = tf.layers.max_pooling2d(conv1, (2, 2), (2, 2), padding='same')

conv2 = tf.layers.conv2d(maxpool1, 32, (3, 3),
                         padding='same', activation=tf.nn.relu)
conv2 = tf.layers.batch_normalization(conv2, axis=3)
maxpool2 = tf.layers.max_pooling2d(conv2, (2, 2), (2, 2), padding='same')

conv3 = tf.layers.conv2d(maxpool2, 16, (3, 3),
                         padding='same', activation=tf.nn.relu)
conv3 = tf.layers.batch_normalization(conv3, axis=3)
encoded = tf.layers.max_pooling2d(conv3, (2, 2), (2, 2), padding='same')

upsample1 = tf.image.resize_nearest_neighbor(encoded, (75, 75))

conv4 = tf.layers.conv2d(upsample1, 16, (3, 3),
                         padding='same', activation=tf.nn.relu)
conv4 = tf.layers.batch_normalization(conv4, axis=3)

upsample2 = tf.image.resize_nearest_neighbor(conv4, (150, 150))

conv5 = tf.layers.conv2d(upsample2, 32, (3, 3),
                         padding='same', activation=tf.nn.relu)
conv5 = tf.layers.batch_normalization(conv5, axis=3)

upsample3 = tf.image.resize_nearest_neighbor(conv5, (230, 230))

conv6 = tf.layers.conv2d(upsample3, 32, (3, 3),
                         padding='same', activation=tf.nn.relu)
conv6 = tf.layers.batch_normalization(conv6, axis=3)

logits = tf.layers.conv2d(
    conv6, 3, (3, 3), padding='same', activation=tf.nn.sigmoid)