# Generated by Django 2.1.7 on 2019-03-28 23:08

from django.db import migrations, models
import goods.models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_auto_20190327_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBootstrap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=goods.models.get_image_filename, verbose_name='Image')),
            ],
        ),
    ]
