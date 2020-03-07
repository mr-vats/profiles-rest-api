from django.urls import path, include
from profiles_api import views

from rest_framework.routers import DefaultRouter


router= DefaultRouter()
#First args -> name of URL,2nd arg-> viewset that we want to register to URL
router.register('hello-viewset',views.HelloViewSet, basename='hello-viewset')

urlpatterns=[
    path('hello-view/',views.HelloApiView.as_view()),
    path('',include(router.urls))



]
