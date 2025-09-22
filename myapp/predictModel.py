# from PIL import Image
# import numpy as np
# import tensorflow as tf
# from keras.layers import TFSMLayer
#
#
# model = TFSMLayer('/home/prajwalsaini/Documents/ai/saved_model/mobilenetv2_model', call_endpoint='serving_default')
#
#
# class_labels = ['Face', 'Fat Body', 'Hair', 'Low-Fat Body', 'Non Human']
#
# # Define the predict function
# def predict(image_path):
#     # Load and preprocess the image
#     image = Image.open(image_path)
#     image = image.resize((224, 224))  # Resize for the model
#     image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
#     image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
#
#
#     predictions = model(image_array)
#
#     # Extract probabilities from the predictions dictionary
#     # Replace 'output_0' with the actual output key of your model
#     predictions_array = predictions['output_0'].numpy()
#
#     # Get the index of the highest probability
#     predicted_index = np.argmax(predictions_array, axis=-1)[0]  # Assuming batch size of 1
#
#     # Map the index to the class label
#     predicted_class = class_labels[predicted_index]
#
#
#         #save image to s3
#
#
#     return predicted_class
#
