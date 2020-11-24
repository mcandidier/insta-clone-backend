from django.db import models

from django.conf import settings

User = settings.AUTH_USER_MODEL

class PostLike(models.Model):
    """ Post Like model
    """
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    """ Post model
    """

    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    is_archived = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, through="PostLike")
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: 
        ordering = ['-id']

    def __str__(self):
        return '{}'.format(self.description)
