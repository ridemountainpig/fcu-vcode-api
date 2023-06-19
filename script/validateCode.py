from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import tensorflow as tf

def validateCode(image_path):
    OriginalImage = Image.open(image_path)
    OriginalImage = OriginalImage.convert('L')

    width, height = OriginalImage.size

    part_width = (width - 12) // 4

    for i in range(4):
        left = i * part_width + 6
        upper = 0
        right = (i + 1) * part_width + 6
        lower = height

        part = OriginalImage.crop((left, upper, right, lower))

        part = part.convert("RGB")

        size = (224, 224)
        image = ImageOps.fit(part, size, Image.LANCZOS)

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model("model/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("model/labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = image.convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)


def validateCodeLite(image_path):
    # Load the TFLite model
    interpreter = tf.lite.Interpreter(model_path="model/keras_model.tflite")
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load the labels
    class_names = open("model/labels.txt", "r").readlines()

    # Load and preprocess the image
    OriginalImage = Image.open(image_path)
    OriginalImage = OriginalImage.convert('L')

    width, height = OriginalImage.size

    part_width = (width - 12) // 4

    for i in range(4):
        left = i * part_width + 6
        upper = 0
        right = (i + 1) * part_width + 6
        lower = height

        part = OriginalImage.crop((left, upper, right, lower))
        part = part.convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(part, size, Image.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.expand_dims(normalized_image_array, axis=0)

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], data)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Get the predicted class index
        predicted_index = np.argmax(output_data)
        class_name = class_names[predicted_index]
        confidence_score = output_data[0][predicted_index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)
