from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Course title")
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_("Course description")
    )
    audio = models.FileField(
        upload_to=MEDIA_ROOT,
        null=True,
        help_text=_("Audio file")
    )

    def __str__(self):
        return self.title.replace(" ", "_")


class VideoCourse(Course):
    video = models.FileField(
        upload_to="videos/"
    )


class PresentationCourse(Course):
    pass


class Slide(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        help_text=_("Course frame"),
        on_delete=models.CASCADE
    )
    number = models.IntegerField(
        default=0,
        help_text=_("Slide number")
    )
    image = models.ImageField(
        upload_to=MEDIA_ROOT,
        help_text=_("Slide image")
    )

    def __str__(self):
        return "_".join([
            str(self.course.title.replace("" "", "_")),
            str(self.number),
            str(self.id)
        ])


class Comment(models.Model):
    slide = models.ForeignKey(
        "courses.Slide",
        help_text=_("Comment to slide"),
        on_delete=models.CASCADE
    )
    # TODO: change to custom user
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        help_text=_("Comment author"),
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=300,
        help_text=_("Comment text")
    )

    def __str__(self):
        return "_".join([
            str(self.author),
            self.text.replace("" "", "_")[:30]
        ])


class CheckPoint(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        help_text=_("Course check point"),
        on_delete=models.CASCADE
    )
    number = models.IntegerField(
        default=0,
        help_text=_("Check point number")
    )
    time = models.FloatField(
        default=.0,
        help_text=_("Check point time in seconds")
    )
    slide_number = models.IntegerField(
        default=0,
        help_text=_("Slide number")
    )

    def __str__(self):
        return "_".join([
            str(self.course)[:10],
            str(self.number),
            str(self.time),
            str(self.slide_number)
        ])
