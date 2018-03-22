from django.contrib import admin

# Register your models here.
from courses.models import Course, Slide, PresentationCourse

admin.site.register(Course)
admin.site.register(PresentationCourse)
admin.site.register(Slide)
