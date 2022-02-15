from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("update/", views.create_update, name="create_update"),
    path("update/<str:title>", views.create_update, name="create_update"),
    path("delete/<title>/<deletion>", views.delete, name="delete"),
    path("random/", views.random_rend, name="random"),
    path("not-found", views.notFound, name="notFound")
]
