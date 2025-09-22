import traceback

import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO



from Models.FaceModel.FacePredict import faceModelCore

from Models.traning.NorwoodVerify import norwoodPredict

model = YOLO("yolov8n.pt")

mp_face_mesh = mp.solutions.face_mesh


def calculate_percentage(mask, total_pixels):
    return (np.sum(mask) / total_pixels) * 100

def process_face_image(image_path):
    try:
        img = cv2.imread(image_path)
        # img= Image.open(image_path).convert('RGB')

        if img is None:
            print(f"Error: Could not load image {image_path}")
            return "Invalid Image", {}

        img = np.array(img)

        results = model(img, conf=0.25)

        imgn=cv2.resize(img,(640,640))

        face_pixel=calculate_face_area(imgn)
        face_img=crop_face(imgn)

        if face_pixel > 0:
          face_data = callFaceModel(face_img,face_pixel)
        else:
            face_data={"details":[]}
            face_data["details"].append({
                "class_name": "No Face Detected",
                "severity": 0.0
            })


        return face_data["details"]

    except Exception as e:
        print(f"Error In Face Prediction Service: {e}")
        traceback.print_exc()


def calculate_face_area(image):

    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:

        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            print("No face detected.")
            return 0

        # Create a blank mask with the same dimensions as the image
        face_mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # Loop through detected faces (if multiple)
        for face_landmarks in results.multi_face_landmarks:
            # Collect landmark points as a list of (x, y) tuples
            points = []
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])  # Convert normalized to pixel
                y = int(landmark.y * image.shape[0])
                points.append((x, y))

            # Create a convex hull around the landmarks
            points = np.array(points, dtype=np.int32)
            hull = cv2.convexHull(points)

            # Draw the filled convex hull on the mask
            cv2.fillConvexPoly(face_mask, hull, 255)

        # Count the non-zero pixels in the mask (face area)
        face_area = np.count_nonzero(face_mask)
        return face_area


def crop_face(image):
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        results = face_mesh.process(rgb_image)

        if results.multi_face_landmarks:

            face_landmarks = results.multi_face_landmarks[0]


            x_min = y_min = float('inf')
            x_max = y_max = float('-inf')

            image_height, image_width, _ = image.shape

            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)

                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)


            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(image_width, x_max + padding)
            y_max = min(image_height, y_max + padding)


            cropped_face = image[y_min:y_max, x_min:x_max]

            return cropped_face
        else:
            print("No face detected.")
            return None



def callFaceModel(imagePath,faceMask):

    data=faceModelCore(imagePath,faceMask)
    if data["summary"] == "Defects detected.":
        return data
    else:
        data["details"].append({
            "class_name": "No defects detected",
            "severity":  0.0
        })
        return data

def callHairModel(imagePath):
    try:
     # baldness model
     baldness = norwoodPredict(imagePath)
     # hair condition model
     hairConditions="dry hair ,thick"
     return [baldness,hairConditions ]
    except Exception as e:
     print(e);
     traceback.print_exc()
     return {f"Error In HairModel {e}"}




