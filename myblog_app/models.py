from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)  # External image URL
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class Signup(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=200)
#     phone = models.CharField(max_length=15)

#     def __str__(self):
#         return self.username


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"
    
    # multiple images
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return f"Image for {self.blog.title}"



class ExploreTopic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='topic_images/')
    badge = models.CharField(max_length=50)
    badge_color = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.title


