import ast
import base64

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework import status

from courses.models import Slide, Course


def courses_catalog(request):
    courses = []
    for course in Course.objects.all():
        cover = Slide.objects.get(course=course, number=0)
        courses.append({'id': course.id,
                        'title': course.title,
                        'description': course.description,
                        'cover': cover.image})

    return render(request, 'courses/catalog.html', {'courses': courses})


def create_course(request):
    return render(request, 'courses/create.html')


def save_course(request):
    course_data = ast.literal_eval(request.POST['course'])
    course = Course.objects.create(
        title=course_data['title'],
        description=course_data['description']
    )

    for slide_data in course_data['slides']:
        f, image_data = slide_data['data'].split(';base64,')
        ext = '.' + f.split('/')[-1]
        image = ContentFile(base64.b64decode(image_data))

        slide = Slide.objects.create(
            course=course,
            number=slide_data['key'],
            image=slide_data['data'].split(',')[1]
        )
        slide.image.save(
            ''.join(['slide', str(slide.id), '_image', str(slide_data['key']), ext]),
            image
        )
    return HttpResponse(status=status.HTTP_200_OK)


def get_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    slides = []
    for slide in Slide.objects.filter(course=course):
        slides.append({'number': slide.number,
                       'image': slide.image})

    return render(request, 'courses/course.html', {'course': course, 'slides': slides})


def delete_course(request, course_id):
    Course.objects.get(pk=course_id).delete()
    return redirect(courses_catalog)
