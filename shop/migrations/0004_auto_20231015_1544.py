# Generated by Django 3.1.4 on 2023-10-15 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_sauthor_sbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sbook',
            name='author',
        ),
        migrations.DeleteModel(
            name='sAuthor',
        ),
        migrations.DeleteModel(
            name='sBook',
        ),
    ]
