import ast
import base64
import json

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from courses.models import Slide, Course, Comment, CheckPoint, Pointer, Point


def courses_catalog(request):
    courses = []
    for course in Course.objects.all():
        cover = Slide.objects.get(course=course, number=0)
        courses.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "cover": cover.image.url
        })

    return render(request, "courses/catalog.html", {"courses": courses})


def search_course(request):
    search_text = json.loads(request.body.decode("utf-8"))["search_text"]

    courses = []
    for course in Course.objects.filter(title__startswith=search_text):
        cover = Slide.objects.get(course=course, number=0)
        courses.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "cover": cover.image.url
        })

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({
                            "courses": courses
                        }),
                        content_type="application/json")


def create_course(request):
    return render(request, "courses/create.html")


def save_course(request):
    course_data = ast.literal_eval(request.POST["course"])
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
        f, image_data = slide_data["image"].split(";base64,")
        ext = "." + f.split("/")[-1]
        image = ContentFile(base64.b64decode(image_data))

        slide = Slide.objects.create(
            course=course,
            number=slide_data["number"],
            name=slide_data["name"],
            image=slide_data["image"].split(",")[1]
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
            slide_name=check_point_data["slide_name"],
            slide_number=check_point_data["slide_number"]
        )

    # Save pointers
    for pointer_data in course_data["pointers"]:
        pointer = Pointer.objects.create(
            course=course,
            start_time=pointer_data["start_time"],
            end_time=pointer_data["end_time"]
        )
        for point_data in pointer_data["points"]:
            point = Point.objects.create(
                pointer=pointer,
                time=point_data["time"],
                left=point_data["left"],
                top=point_data["top"]
            )

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({"course_id": course.id}),
                        content_type="application/json")


def get_course_data(course_id):
    course = Course.objects.get(pk=course_id)
    author = course.author

    slides = []
    for slide in Slide.objects.filter(course=course):
        comments = []
        for comment in Comment.objects.filter(slide=slide):
            comments.append({
                "id": comment.id,
                "slide_id": comment.slide.id,
                "author_id": comment.author.id if comment.author else -1,
                "author_name": comment.author.username if comment.author.username else "",
                "text": comment.text
            })
        slides.append({
            "id": slide.pk,
            "number": slide.number,
            "name": slide.name,
            "image": slide.image.url,
            "comments": comments
        })

    check_points = []
    for check_point in CheckPoint.objects.filter(course=course):
        check_points.append({
            "id": check_point.id,
            "number": check_point.number,
            "time": check_point.time,
            "slide_name": check_point.slide_name,
            "slide_number": check_point.slide_number
        })

    pointers = []
    for pointer in Pointer.objects.filter(course=course):
        points = []
        for point in Point.objects.filter(pointer=pointer):
            points.append({
                "id": point.id,
                "time": point.time,
                "left": point.left,
                "top": point.top
            })
        pointers.append({
            "id": pointer.id,
            "start_time": pointer.start_time,
            "end_time": pointer.end_time,
            "points": points
        })

    return {"course": course,
            "author": author,
            "slides": slides,
            "check_points": check_points,
            "pointers": pointers}


def get_course(request, course_id):
    course_data = get_course_data(course_id)
    return render(request, "courses/course.html", course_data)


def change_course_page(request, course_id):
    course_data = get_course_data(course_id)
    return render(request, "courses/change.html", course_data)


def change_course(request):
    course_data = json.loads(request.body.decode("utf-8"))
    course = Course.objects.get(pk=course_data["course_id"])

    course.title = course_data["title"]
    course.description = course_data["description"]

    CheckPoint.objects.filter(course=course).delete()
    for check_point_data in course_data["check_points"]:
        check_point = CheckPoint.objects.create(
            course=course,
            number=check_point_data["number"],
            time=check_point_data["time"],
            slide_name=check_point_data["slide_name"],
            slide_number=check_point_data["slide_number"]
        )

    Pointer.objects.filter(course=course).delete()
    for pointer_data in course_data["pointers"]:
        pointer = Pointer.objects.create(
            course=course,
            start_time=pointer_data["start_time"],
            end_time=pointer_data["end_time"]
        )
        for point_data in pointer_data["points"]:
            point = Point.objects.create(
                pointer=pointer,
                time=point_data["time"],
                left=point_data["left"],
                top=point_data["top"]
            )
    course.save()

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({"course_id": course.id}),
                        content_type="application/json")


def delete_course(request, course_id):
    Course.objects.get(pk=course_id).delete()
    return redirect(courses_catalog)


@csrf_exempt
def save_comment(request):
    comment_data = json.loads(request.body.decode("utf-8"))
    author = User.objects.get(username=request.user.username)
    comment = Comment.objects.create(
        text=comment_data["text"],
        author=author,
        slide=Slide.objects.get(pk=comment_data["slide_id"])
    )
    return HttpResponse(status=status.HTTP_200_OK,
                        content_type="application/json",
                        content=json.dumps({
                            "id": comment.id,
                            "slide_id": comment.slide.id,
                            "author_id": comment.author.id if comment.author.id else -1,
                            "author_name": comment.author.username if comment.author.username else "",
                            "text": comment.text
                        }))
