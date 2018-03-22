from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Course title')
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_('Course description')
    )

    def __str__(self):
        return self.title


class VideoCourse(Course):
    video = models.FileField(
        upload_to='videos/'
    )


class PresentationCourse(Course):
    pass


class Slide(models.Model):
    course = models.ForeignKey(
        'courses.Course',
        help_text=_('Course frame'),
        on_delete=models.CASCADE
    )
    number = models.IntegerField(
        default=0,
        help_text=_('Slide number')
    )
    image = models.ImageField(
        upload_to=MEDIA_ROOT,
        help_text=_('Slide image')
    )

    def __str__(self):
        return ''.join([str(self.course.title), '_slide', str(self.number)])
