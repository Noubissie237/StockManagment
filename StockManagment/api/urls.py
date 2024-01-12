
from django.contrib import admin
from django.urls import path
from .views import CurrenTimeView, ShopAPIView

urlpatterns = [
    path('time/', CurrenTimeView.as_view()),
    path('shop/', ShopAPIView.as_view(), name='shop-api'),


]
