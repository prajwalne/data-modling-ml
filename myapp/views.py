import base64
import json
import traceback
from operator import truediv

from django.shortcuts import render
# myapp/views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from Models.FaceModel.FaceModel import getFaceData
from Models.HairModel.HairModel import getHairData
from Models.HairModel.HairPredict import hair_model_core
from Models.traning.NorwoodVerify import norwoodPredict
# from .predictionService import process_image
import logging

import speech_recognition as sr
from pydub import AudioSegment
import requests

from myapp.predictionService import callFaceModel

log =logging.getLogger(__name__)
def home(request):
    return HttpResponse("Hello, from Django!")

@csrf_exempt
def checkapi(request):
    log.info("in checkapi method")
    return JsonResponse({'success': True, 'message': "sup"})





@csrf_exempt
def norwood_predict(request):
    if(request.method=='POST' and request.FILES.get('image')):
        uploaded_file=request.FILES.get('image')
        file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        full_path = os.path.join(default_storage.location, file_path)
        try:
            # Call your model prediction function
            result =  norwoodPredict(full_path)

            if result.startswith("Error in prediction:"):
                return JsonResponse({'success': False, 'error': result})
            else:
                return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            print(f"Error in Norwood Controller: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        finally:
            # Clean up: delete the uploaded file after processing
            if os.path.exists(full_path):
                os.remove(full_path)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@csrf_exempt
def test(request):

    if(request.method=='POST' and request.FILES.get('image')):
        uploaded_file=request.FILES.get('image')
        file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        full_path = os.path.join(default_storage.location, file_path)
        try:
            # Call your model prediction function
            print("going_In_hair_modle_fuction")
            # result =  callFaceModel(full_path)
            # print(result)
            result=list(hair_model_core(full_path))
            # print("here are the results ",result)
            return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            print(f"Error in test face  Controller: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        finally:
            # Clean up: delete the uploaded file after processing
            if os.path.exists(full_path):
                os.remove(full_path)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def test2(request):

        if (request.method == 'POST' and request.FILES.get('image')):
            uploaded_file = request.FILES.get('image')
            file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            full_path = os.path.join(default_storage.location, file_path)
            try:
                # Call your model prediction function
                # result = face_model_core(full_path)
                # print(result)
                # result="success"
                result=""

                if result.startswith("Error in prediction:"):
                    return JsonResponse({'success': False, 'error': result})
                else:
                    return JsonResponse({'success': True, 'prediction': result})
            except Exception as e:
                print(f"Error in test face  Controller: {e}")
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            finally:
                # Clean up: delete the uploaded file after processing
                if os.path.exists(full_path):
                    os.remove(full_path)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def face(request):
    if (request.method == 'POST' and request.FILES.get('image')):
        uploaded_file = request.FILES.get('image')
        file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        full_path = os.path.join(default_storage.location, file_path)
        try:
            # Call your model prediction function
            log.info("In Face Controller")

            result = getFaceData(full_path)

            result=list(result);

            # if result.startswith("Error in prediction:"):
            #     return JsonResponse({'success': False, 'error': result})
            # else:
            return JsonResponse({'success': True, 'detections': result})
        except Exception as e:
            error=f"Error in face  Controller: {e}"
            log.error(error)
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        finally:
            # Clean up: delete the uploaded file after processing
            if os.path.exists(full_path):
                os.remove(full_path)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)



@csrf_exempt
def hair(request):
    if (request.method == 'POST' and request.FILES.get('image')):
        uploaded_file = request.FILES.get('image')
        file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        full_path = os.path.join(default_storage.location, file_path)
        try:
            # Call your model prediction function
            print("In hair controller")
            result = getHairData(full_path)
            result=list(result);
            # print(result)

            # if result.startswith("Error in prediction:"):
            #     return JsonResponse({'success': False, 'error': result})
            # else:
            return JsonResponse({'success': True, 'detections': result})
        except Exception as e:
            error=f"Error in face  Controller: {e}"
            log.error(error)
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        finally:
            # Clean up: delete the uploaded file after processing
            if os.path.exists(full_path):
                os.remove(full_path)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def decode_base64_file(data, filename):
    ext = "jpg"
    file_name = f"{filename}.{ext}"
    file_path = default_storage.save(file_name, ContentFile(base64.b64decode(data)))
    return os.path.join(default_storage.location, file_path)


@csrf_exempt
def processFaceAndHair(request):
    if request.method == 'POST':
        try:
            print("FIRST LINE->", request,flush=True);
            data = json.loads(request.body)
            print("request Body->",data);
            hair_image_base64 = data.get('base64_image_hair_image')
            face_image_base64 = data.get('base64_image_face_image')
            print("in controler");
            print("Looking good ");


            # print("Base 64 hair image",hair_image_base64, flush=True)
            # print("Base 64 face image",hair_image_base64, flush=True)

            if not hair_image_base64 or not face_image_base64:
                return JsonResponse({'success': False, 'error': 'Missing base64 images'}, status=400)

            # Decode and save images
            hair_image_path = decode_base64_file(hair_image_base64, "hair_image")
            face_image_path = decode_base64_file(face_image_base64, "face_image")

            # Get face and hair data
            face_result = list(getFaceData(face_image_path))
            hair_result = list(hair_model_core(hair_image_path))

            # Ensure results are strings
            face_condition = ", ".join(map(str, face_result)) if isinstance(face_result, (list, set)) else str(
                face_result)
            hair_condition = ", ".join(map(str, hair_result)) if isinstance(hair_result, (list, set)) else str(
                hair_result)

            response = {
                'hair_condition': hair_condition,
                'face_condition': face_condition
            }




            response = {
                'hair_condition': list(hair_result),
                'face_condition': list(face_result)
            }

            print("Here is the response: ",response);

            return JsonResponse({'success': True, 'data': response})

        except Exception as e:
            error_msg = f"Error processing face and hair: {e}"
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': error_msg}, status=500)

        finally:
            # Clean up files
            if os.path.exists(hair_image_path):
                os.remove(hair_image_path)
            if os.path.exists(face_image_path):
                os.remove(face_image_path)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def recognizeSpeechToText(request):

    def convert_mp3_to_wav(mp3_path, wav_path):
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

    print("here")
    data = json.loads(request.body)
    mp3_url = data.get("mp3_url")
    local_mp3 = 'audio.mp3'
    local_wav = 'audio.wav'

    try:
        if not mp3_url:
            return JsonResponse({'success': False, 'error': 'Missing data'}, status=400)
        else:
            response = requests.get(mp3_url)
            if response.status_code == 200:
                with open(local_mp3, 'wb') as f:
                    f.write(response.content)
            else:
                return JsonResponse({'success': False, 'error': 'Failed to download MP3 from mp3_file'}, status=400)
            convert_mp3_to_wav(local_mp3,local_wav)

        if request.method == 'POST':
            recognizer = sr.Recognizer()
            with sr.AudioFile(local_wav) as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                print(text)
                return JsonResponse({'message': text, 'success': True})
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    finally:
        for file in [local_mp3, local_wav]:
            if os.path.exists(file):
                os.remove(file)
