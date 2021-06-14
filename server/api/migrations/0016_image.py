# Generated by Django 3.0.8 on 2021-06-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20210614_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('box_info', models.TextField(blank=True, null=True)),
                ('count_assigned', models.IntegerField(default=0)),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]
