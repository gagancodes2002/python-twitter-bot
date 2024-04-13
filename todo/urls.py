from django.urls import path
from .views import homeView, completeTaskView, editTaskView, deleteTaskView,deleteAllTaskView

urlpatterns = [
    path("", homeView, name="homeView"),
    path("complete/<id>", completeTaskView, name="completeTaskView"),
    path("edit/<id>", editTaskView, name="editTaskView"),
    path("delete/<id>", deleteTaskView, name="deleteTaskView"),
    path("delete/", deleteAllTaskView, name="deleteAllTaskView"),
]
