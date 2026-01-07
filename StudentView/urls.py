from . import views
from django.urls import path

urlpatterns = [
    path("add_manually_post", views.add_manually_post, name="add_manually_post"),
    path("submitted", views.submitted, name="submitted"),
    path("attendance_error", views.attendance_error, name="attendance_error"),
]
