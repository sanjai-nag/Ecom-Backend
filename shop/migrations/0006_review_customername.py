# Generated by Django 3.1.4 on 2023-10-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='customername',
            field=models.CharField(default='null', max_length=100),
        ),
    ]
