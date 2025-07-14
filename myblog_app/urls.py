from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home_app, name='index'),
    path('category/<int:cat_id>/', views.blogs_by_category, name='blogs_by_category'),  
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blogform/', views.BlogForm, name='write'),
    path('sign-in/', views.user_Signup, name='sign-up'),
    path('user-login/', views.loginUser, name="log-in"),
    path('logout/', views.logout_view, name='user-logout'),
    path('contact/', views.contact_view, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/<int:user_id>/', views.reset_password_view, name='reset-password'),
    path('edit-blog/<int:id>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
     # Instead of: path('explore/<slug:slug>/', ...)
path('explore/<int:id>/', views.explore_topic_detail, name='explore_topic'),


] 

