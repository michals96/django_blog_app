# Generated by Django 2.2.1 on 2019-05-29 18:22

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', embed_video.fields.EmbedVideoField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
