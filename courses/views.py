import ast
import base64
import json

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from courses.models import Slide, Course, Comment, CheckPoint


def courses_catalog(request):
    courses = []
    for course in Course.objects.all():
        cover = Slide.objects.get(course=course, number=0)
        courses.append({"id": course.id,
                        "title": course.title,
                        "description": course.description,
                        "cover": cover.image})

    return render(request, "courses/catalog.html", {"courses": courses})


def create_course(request):
    return render(request, "courses/create.html")


def save_course(request):
    course_data = ast.literal_eval(request.POST["course"])
    print(course_data["pointers"])
    author = User.objects.get(username=request.user.username)

    course = Course.objects.create(
        author=author,
        title=course_data["title"],
        description=course_data["description"],
    )

    # Save audio file data
    f, audio_data = course_data["audio"]["data"].split(";base64,")
    ext = "." + f.split("/")[-1]
    audio = ContentFile(base64.b64decode(audio_data))
    course.audio.save(
        "".join([course_data["audio"]["name"], ext]),
        audio
    )

    # Save slides data
    for slide_data in course_data["slides"]:
        f, image_data = slide_data["data"].split(";base64,")
        ext = "." + f.split("/")[-1]
        image = ContentFile(base64.b64decode(image_data))

        slide = Slide.objects.create(
            course=course,
            number=slide_data["number"],
            image=slide_data["data"].split(",")[1]
        )
        slide.image.save(
            "".join(["slide", str(slide.id), "_image", str(slide_data["number"]), ext]),
            image
        )

    # Save checkpoints
    for check_point_data in course_data["check_points"]:
        check_point = CheckPoint.objects.create(
            course=course,
            number=check_point_data["number"],
            time=check_point_data["time"],
            slide_number=check_point_data["slide_number"]
        )

    return HttpResponse(status=status.HTTP_200_OK)


def get_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    author = course.author
    slides = []
    check_points = []
    for check_point in CheckPoint.objects.filter(course=course):
        check_points.append({"number": check_point.number,
                             "time": check_point.time,
                             "slide_number": check_point.slide_number})

    for slide in Slide.objects.filter(course=course):
        comments = []
        for comment in Comment.objects.filter(slide=slide):
            comments.append({
                "id": comment.id,
                "slide_id": comment.slide.id,
                "author_id": comment.author.id if comment.author else -1,
                "author_name": comment.author if comment.author else "",
                "text": comment.text
            })
        slides.append({"id": slide.pk,
                       "number": slide.number,
                       "image": slide.image,
                       "comments": comments})

    return render(request, "courses/course.html", {"course": course,
                                                   "author": author,
                                                   "slides": slides,
                                                   "check_points": check_points})


def delete_course(request, course_id):
    Course.objects.get(pk=course_id).delete()
    return redirect(courses_catalog)


@csrf_exempt
def save_comment(request):
    comment_data = json.loads(request.body.decode("utf-8"))
    comment = Comment.objects.create(
        text=comment_data["text"],
        slide=Slide.objects.get(pk=comment_data["slide_id"])
    )
    return HttpResponse(status=status.HTTP_200_OK,
                        content_type="application/json",
                        content=json.dumps({
                            "id": comment.id,
                            "slide_id": comment.slide.id,
                            "author_id": comment.author.id if comment.author else -1,
                            "author_name": comment.author if comment.author else """""",
                            "text": comment.text
                        }))
