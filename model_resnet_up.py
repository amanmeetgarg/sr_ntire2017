import tensorflow as tf
import util

upsample = True

def build_model(x, scale, training, reuse):
    hidden_size = 128
    bottleneck_size = 32
    x = tf.layers.conv2d(x, hidden_size, 1, activation=None, name='in', reuse=reuse)
    for i in range(5):
        x = util.crop_by_pixel(x, 1) + conv(x, hidden_size, bottleneck_size, training, 'lr_conv'+str(i), reuse)
    x = tf.nn.relu(x)
    x = tf.layers.conv2d_transpose(x, hidden_size, scale, strides=scale, activation=None, name='up', reuse=reuse)
    for i in range(5):
        x = util.crop_by_pixel(x, 1) + conv(x, hidden_size, bottleneck_size, training, 'hr_conv'+str(i), reuse)
    x = tf.nn.relu(x)
    x = tf.layers.conv2d(x, 3, 1, activation=None, name='out', reuse=reuse)
    return x

def conv(x, hidden_size, bottleneck_size, training, name, reuse):
    x = tf.nn.relu(x)
    x = tf.layers.conv2d(x, bottleneck_size, 1, activation=None, name=name+'_proj', reuse=reuse)
    
    x = tf.nn.relu(x)
    x = tf.layers.conv2d(x, bottleneck_size, 3, activation=None, name=name+'_filt', reuse=reuse)
    
    x = tf.nn.relu(x)
    x = tf.layers.conv2d(x, hidden_size, 1, activation=None, name=name+'_recv', reuse=reuse)
    return x