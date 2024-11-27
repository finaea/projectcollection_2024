import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import seaborn as sn

#importing the dataset from keras dataset into train and testing dataset
(X_train, y_train) , (X_test, y_test) = keras.datasets.mnist.load_data()

#normilizing the data, so it will provide value from 0 to 1
X_train = X_train / 255
X_test = X_test / 255

#flattening the data, we are just turing 2d array to 1d array
X_train_flattened = X_train.reshape(len(X_train), 28*28)
X_test_flattened = X_test.reshape(len(X_test), 28*28)

#now we build the model. we are building with 1 hidden layer , in total there are 3 layers
# input layer consists 784 nuerons -> represnts one image
# hidden layer consists of 100 nuerons -> completely random
# droupout layer to prevent overfitting
# output layer consists of 10 nuerons -> represents the predicted value from 0 to 9

model = keras.Sequential()
model.add(keras.layers.Dense(784, input_shape=(784,), activation='relu'))  # Input layer with 784 neurons
model.add(keras.layers.Dense(100, activation='relu'))  # Hidden layer with 100 neurons
model.add(keras.layers.Dropout(0.25))  # Add dropout layer with 0.25
model.add(keras.layers.Dense(10, activation='softmax'))  # Output layer with 10 neurons (using softmax for multi-class classification)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#we are training the data with images, with 10 iterations
history = model.fit(X_train_flattened, y_train, epochs=10, validation_split = 0.2)

#now we are evaluating the trained model with a test data, adn we want to see the acuracy
print('\n################################# \n Evaluating the model with test data\n')
model.evaluate(X_test_flattened,y_test)

#now we are building confusion matrix
y_predicted = model.predict(X_test_flattened)
y_predicted_labels = [np.argmax(i) for i in y_predicted]
cm = tf.math.confusion_matrix(labels=y_test,predictions=y_predicted_labels)

plt.figure(figsize = (10,7))
sn.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.show()

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
