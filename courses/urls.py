from django.urls import path

from .views import *

urlpatterns = [
    path(r"", courses_catalog, name="courses_catalog"),
    path(r"create_course", create_course, name="create_course"),
    path(r"save_course", save_course, name="save_course"),
    path(r"get_course/<course_id>", get_course, name="get_course"),
    path(r"delete_course/<course_id>", delete_course, name="delete_course"),
    path(r"save_slide_comment", save_comment, name="save_slide_comment")
]
