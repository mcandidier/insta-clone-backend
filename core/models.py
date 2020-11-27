from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    timestamp = models.DateTimeField(auto_now_add=True)


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
