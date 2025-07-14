from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Blog, Contact, Comment, Category, ExploreTopic
from .forms import BlogPostForm, LoginForm, ContactForm, ForgotPasswordForm, CustomSignupForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import datetime

# Home Page – Shows tech stack + categories + blogs
from .models import Blog, Category, ExploreTopic
import datetime

def home_app(request):
    tech_stack = "HTML,CSS,Bootstrap,JavaScript,React,Python,Django".split(',')
    blogs = Blog.objects.all().order_by('-created_at')[:6]  # latest 6 blogs
    categories = Category.objects.all()  # get all categories
    today_date = datetime.date.today().strftime("%B %d, %Y")
    topics = ExploreTopic.objects.all() 

    return render(request, 'app-index.html', {
        'tech_stack': tech_stack,
        'blogs': blogs,
        'categories': categories,
        'topics': topics,  
        'today_date': today_date
    })



# Blog List View – All blogs


def blog_list(request):
    query = request.GET.get('q')
    
    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
        
    return render(request, 'blog_list.html', {'blogs': blogs})

# Blog Detail View – Single blog
def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all().order_by('-created_at')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog
                comment.save()
                messages.success(request, "Comment posted successfully!")
                return redirect('blog_detail', id=blog.id)
        else:
            messages.error(request, "You need to login to comment.")
            return redirect('log-in')
    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'form': form,
        'comments': comments
    })
@login_required(login_url='log-in')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    blog_id = comment.blog.id  # store before deleting

    if comment.user != request.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('blog_detail', id=blog_id)

    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('blog_detail', id=blog_id)

# Blog Form – Only for logged-in users
@login_required(login_url='log-in')
def BlogForm(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog posted successfully!")
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog_pform.html', {'form': form})

# User Signup – Built-in User model
def user_Signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            messages.success(request, "Signup successful!")
            return redirect('dashboard')
    else:
        form = CustomSignupForm()
    return render(request, 'sign-up.html', {'form': form})

# User Login
def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'log-in.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('log-in')

# Dashboard – User's own blogs

from django.utils.timezone import localtime

@login_required(login_url='log-in')
def dashboard(request):
    user = request.user
    user_blogs = Blog.objects.filter(author=user).order_by('-created_at')
    
    context = {
        'blogs': user_blogs,
        'total_blogs': user_blogs.count(),
        'last_login': localtime(user.last_login).strftime("%B %d, %Y at %I:%M %p") if user.last_login else "N/A",
        'date_joined': localtime(user.date_joined).strftime("%B %d, %Y"),
    }
    return render(request, 'dashboard.html', context)


# Contact Form View  
def contact_view(request):
    if request.method == "POST":
        cform = ContactForm(request.POST)
        if cform.is_valid():
            Contact.objects.create(
                name=cform.cleaned_data['name'],
                email=cform.cleaned_data['email'],
                subject=cform.cleaned_data['subject'],
                message=cform.cleaned_data['message']
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('index')
    else:
        cform = ContactForm()
    return render(request, 'contact.html', {'form': cform})

# Forgot Password – Email-based lookup
def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                return redirect('reset-password', user_id=user.id)  # 👈 redirect using user_id
            except User.DoesNotExist:
                form.add_error('email', 'No account found with this email.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})
# Reset Password – Set new password

def reset_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('log-in')

    return render(request, 'reset_password.html', {'user': user})

# edit view
@login_required(login_url='log-in')
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id, author=request.user)  # secure fetch

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'edit.html', {'form': form})

# delete view
@login_required(login_url='log-in')
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.delete()
    messages.success(request, "Blog deleted successfully.")
    return redirect('dashboard')

# delete comment
@login_required(login_url='log-in')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this comment.")

    return redirect('blog_detail', id=comment.blog.id)

# categorized
def blogs_by_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    blogs = Blog.objects.filter(category=category).order_by('-created_at')
    return render(request, 'blogs_by_category.html', {
        'category': category,
        'blogs': blogs
    })
    

def explore_topic_detail(request, id):
    topic = get_object_or_404(ExploreTopic, id=id)
    return render(request, 'explore_topic.html', {'topic': topic})
