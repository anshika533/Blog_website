from django.contrib import admin
from .models import Blog,Contact, Comment, Category, ExploreTopic

admin.site.register(Blog)
# admin.site.register(Signup)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ExploreTopic)