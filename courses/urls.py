from django.urls import path

from .views import *

urlpatterns = [
    path(r"", courses_catalog, name="courses_catalog"),
    path(r"search_course", search_course, name="search_course"),
    path(r"create_course", create_course, name="create_course"),
    path(r"save_course", save_course, name="save_course"),
    path(r"change_course", change_course, name="change_course"),
    path(r"change_course_page/<course_id>", change_course_page, name="change_course_page"),
    path(r"get_course/<course_id>", get_course, name="get_course"),
    path(r"change_course/<course_id>", change_course, name="change_course"),
    path(r"delete_course/<course_id>", delete_course, name="delete_course"),
    path(r"save_slide_comment", save_comment, name="save_slide_comment")
]
