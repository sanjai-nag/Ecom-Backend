# Generated by Django 3.1.4 on 2023-10-15 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20231015_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(default='null', max_length=100)),
                ('comments', models.CharField(default='null', max_length=100)),
            ],
        ),
    ]
