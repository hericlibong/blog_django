# Generated by Django 5.1.5 on 2025-02-15 18:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=ckeditor.fields.RichTextField(help_text='Full text of the project', max_length=5000),
        ),
    ]
