from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path(r"", courses_catalog, name="courses_catalog"),
    path(r"search_courses/", search_courses, name="search_courses"),
    path(r"create_course/", create_course, name="create_course"),
    path(r"save_course", save_course, name="save_course"),
    path(r"change_course/", change_course, name="change_course"),
    path(r"change_course_page/<int:course_id>/", change_course_page, name="change_course_page"),
    path(r"get_course/<int:course_id>/", get_course, name="get_course"),
    path(r"change_course/<int:course_id>/", change_course, name="change_course"),
    path(r"delete_course/<int:course_id>/", delete_course, name="delete_course"),
    path(r"save_slide_comment/", save_comment, name="save_slide_comment")
]
