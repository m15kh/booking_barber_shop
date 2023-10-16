from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg' )


    class Meta:
        db_table = 'blog_post'
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail_post', args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        return self.comment
    
    def get_absolute_url(self):
        return reverse('blog:all_post')
    

    