# Generated by Django 2.0.1 on 2018-04-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_slide_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='slide_name',
            field=models.CharField(default='', help_text='Slide name', max_length=100),
        ),
    ]
