from django.urls import path

from . import views

urlpatterns = [
    path("/menu", views.order_view, name="orders")
]