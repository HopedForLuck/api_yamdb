# Generated by Django 3.2 on 2023-09-28 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_review_unique_author_title'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_title',
        ),
    ]
