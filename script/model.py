import tensorflow as tf

# Load your TensorFlow model
model = tf.keras.models.load_model('model/keras_model.h5')

# Convert the model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model to a file
with open('model/keras_model.tflite', 'wb') as f:
    f.write(tflite_model)
