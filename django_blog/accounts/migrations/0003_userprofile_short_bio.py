# Generated by Django 5.1.5 on 2025-02-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='short_bio',
            field=models.CharField(blank=True, help_text='Your short bio for the template profile', max_length=255, null=True),
        ),
    ]
