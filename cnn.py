import tflearn
from tflearn.activations import relu
from tflearn.data_augmentation import ImageAugmentation
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.core import dropout, flatten, fully_connected, input_data
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import (batch_normalization, local_response_normalization)
from tflearn.optimizers import SGD, Adam, Momentum, RMSProp
from tflearn.metrics import Accuracy, R2, WeightedR2, Top_k

img_prep = ImagePreprocessing()
# img_prep.add_featurewise_zero_center()
# img_prep.add_featurewise_stdnorm()

img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_blur(sigma_max=25.)
img_aug.add_random_rotation(max_angle=10.)
# img_aug.add_random_crop((32, 32), 6) # might need to be changed in case of different image size


def get_network_architecture(image_width, image_height, number_of_classes, learning_rate):

    number_of_channels = 1

    network = input_data(
        shape=[None, image_width, image_height, number_of_channels],
        data_preprocessing=img_prep,
        data_augmentation=img_aug,
        name='InputData'
    )

    """
        def conv_2d(incoming, nb_filters, filter_size, strides=1, padding='same',
                    activation='linear', bias='True', weights_init='uniform_scaling',
                    bias_init='zeros', regularizer=None, weight_decay=0.001,
                    trainable=True, restore=True, reuse=False, scope=None,
                    name='Conv2D')

        network = conv_2d(network, 32, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_1')
        network = max_pool_2d(network, (2, 2), strides=2, padding='same', name='MaxPool2D_1')
        network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_1')
        network = dropout(network, 0.5, name='Dropout_1')
        network = batch_normalization(network, name='BatchNormalization')
        network = flatten(network, name='Flatten')
        network = fully_connected(network, 512, activation='relu', name='FullyConnected_1')
        network = fully_connected(network, number_of_classes, activation='softmax', name='FullyConnected_Final')

        print('  {}: {}'.format('Conv2D................', network.shape))
        print('  {}: {}'.format('MaxPool2D.............', network.shape))
        print('  {}: {}'.format('Dropout...............', network.shape))
        print('  {}: {}'.format('BatchNormalization....', network.shape))
        print('  {}: {}'.format('Flatten...............', network.shape))
        print('  {}: {}'.format('FullyConnected........', network.shape))
        print('  {}: {}'.format('FullyConnected_Final..', network.shape))

        CONV / FC -> Dropout -> BN -> activation function -> ...

        Convolutional filters: { 32, 64, 128 }
        Convolutional filter sizes: { 1, 3, 5, 11 }
        Convolutional strides: 1
        Activation: ReLu

        Pooling kernel sizes: { 2, 3, 4, 5 }
        Pooling kernel strides: 2

        Dropout probability: 0.5
            - Higher probability of keeping in earlier stages
            - Lower probability of keeping in later stages
    """

    print('\nNetwork architecture:')
    print('  {}: {}'.format('InputData.............', network.shape))

    network = conv_2d(network, 16, (7, 7), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_1')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_1')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = conv_2d(network, 16, (7, 7), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_2')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_2')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_1')
    print('  {}: {}'.format('AvgPool2D.............', network.shape))
    network = dropout(network, 0.5, name='Dropout_1')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = conv_2d(network, 32, (5, 5), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_3')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_3')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = conv_2d(network, 32, (5, 5), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_4')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_4')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_2')
    print('  {}: {}'.format('AvgPool2D.............', network.shape))
    network = dropout(network, 0.5, name='Dropout_2')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = conv_2d(network, 64, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_5')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_5')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = conv_2d(network, 64, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_6')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_6')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_3')
    print('  {}: {}'.format('AvgPool2D.............', network.shape))
    network = dropout(network, 0.5, name='Dropout_3')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = conv_2d(network, 128, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_7')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_7')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = conv_2d(network, 128, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_8')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_8')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_4')
    print('  {}: {}'.format('AvgPool2D.............', network.shape))
    network = dropout(network, 0.5, name='Dropout_4')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = conv_2d(network, 256, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_9')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_9')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = conv_2d(network, 256, (3, 3), strides=1, padding='same', activation='relu', regularizer='L2', name='Conv2D_10')
    print('  {}: {}'.format('Conv2D................', network.shape))
    network = batch_normalization(network, name='BatchNormalization_10')
    print('  {}: {}'.format('BatchNormalization....', network.shape))
    network = avg_pool_2d(network, (2, 2), strides=2, padding='same', name='AvgPool2D_5')
    print('  {}: {}'.format('AvgPool2D.............', network.shape))
    network = dropout(network, 0.5, name='Dropout_5')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = flatten(network, name='Flatten')
    print('  {}: {}'.format('Flatten...............', network.shape))


    network = fully_connected(network, 512, activation='relu', name='FullyConnected_1')
    print('  {}: {}'.format('FullyConnected........', network.shape))
    network = dropout(network, 0.5, name='Dropout_6')
    print('  {}: {}'.format('Dropout...............', network.shape))


    network = fully_connected(network, number_of_classes, activation='softmax', name="FullyConnected_Final")
    print('  {}: {}'.format('FullyConnected_Final..', network.shape))


    optimizer = Adam(learning_rate=learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-08, use_locking=False, name='Adam')
    # optimizer = SGD(learning_rate=learning_rate, lr_decay=0.01, decay_step=100, staircase=False, use_locking=False, name='SGD')
    # optimizer = RMSProp(learning_rate=learning_rate, decay=0.9, momentum=0.9, epsilon=1e-10, use_locking=False, name='RMSProp')
    # optimizer = Momentum(learning_rate=learning_rate, momentum=0.9, lr_decay=0.01, decay_step=100, staircase=False, use_locking=False, name='Momentum')

    metric = Accuracy(name='Accuracy')
    # metric = R2(name='Standard Error')
    # metric = WeightedR2(name='Weighted Standard Error')
    # metric = Top_k(k=6, name='Top K')


    network = regression(
        network,
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metric=metric,
        learning_rate=learning_rate,
        name='Regression'
    )

    return network


if __name__ == '__main__':
    get_network_architecture(64, 64, 7, 0)

    print('\nArchitecture sample based on input of 32x32 with 2 output classes.')
