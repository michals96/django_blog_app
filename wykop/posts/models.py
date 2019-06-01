from django.db import models
from django.db.models import deletion
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel
from embed_video.fields import EmbedVideoField

from wykop.accounts.models import User


class Post(models.Model):
    title = models.CharField(default='', max_length=150)
    text = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, deletion.PROTECT)
    image = models.ImageField(upload_to='post_images/', blank=True)
    video = EmbedVideoField(null=True,blank=True) 
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})


class Vote(models.Model):
    class Meta:
        unique_together = (
            ('user', 'post'),
        )
    PLUS = 1
    MINUS = -1
    VALUE_CHOICES = (
        (PLUS, '+'),
        (MINUS, '-'),
    )
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(User, deletion.PROTECT, related_name='votes')
    post = models.ForeignKey(Post, deletion.PROTECT, related_name='votes')

    def __str__(self):
        return '({}) {} - {}'.format(
            self.get_value_display(),
            self.user,
            self.post,
        )

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post,deletion.PROTECT,related_name='comments')
    user = models.ForeignKey(User,deletion.PROTECT, related_name='comments')
    text = models.TextField(default='')