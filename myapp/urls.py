from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('predict/', views.predict_image, name='predict_image'),
    path('norwood/', views.norwood_predict),
    path('test/',views.test),
    path('test2/',views.test2),
    path('face/',views.face),
    path('hair/',views.hair),
    path('checkapi/', views.checkapi),
    path('nlp/', views.recognizeSpeechToText),
    path('processFaceAndHair/', views.processFaceAndHair)



]