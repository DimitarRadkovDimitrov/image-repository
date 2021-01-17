# Generated by Django 3.1.5 on 2021-01-15 01:39

from django.conf import settings
from django.db import migrations, models
import image_marketplace.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_private', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('storage_id', models.CharField(max_length=36)),
                ('height', models.FloatField()),
                ('width', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=models.SET(image_marketplace.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'title')},
            },
        ),
    ]