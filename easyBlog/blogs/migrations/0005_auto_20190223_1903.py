# Generated by Django 2.1.1 on 2019-02-23 11:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20190223_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
