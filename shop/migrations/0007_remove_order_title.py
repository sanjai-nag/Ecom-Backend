# Generated by Django 3.1.4 on 2023-10-21 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_review_customername'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='title',
        ),
    ]
