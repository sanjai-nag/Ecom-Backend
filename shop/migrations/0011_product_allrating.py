# Generated by Django 3.1.4 on 2023-10-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20231021_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allrating',
            field=models.IntegerField(default=0),
        ),
    ]