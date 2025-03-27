from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BlogPost


# Render login page
def login_page(request):
    return render(request, "login.html")  

# User Registration
def register(request):
    context = {}
    if request.method == "POST":
        un = request.POST["username"]
        em = request.POST["email"]
        p = request.POST["password"]
        cp = request.POST["confirm_password"]

        # Validation checks
        if un == "" or em == "" or p == "" or cp == "":
            context["error_msg"] = "All fields are required!"
            return render(request, 'register.html', context)
        elif len(p) < 8:
            context["error_msg"] = "Password must be at least 8 characters!"
            return render(request, 'register.html', context)
        elif p != cp:
            context["error_msg"] = "Passwords do not match!"
            return render(request, 'register.html', context)
        elif User.objects.filter(username=un).exists():
            context["error_msg"] = "Username already exists!"
            return render(request, 'register.html', context)
        elif User.objects.filter(email=em).exists():
            context["error_msg"] = "Email already exists!"
            return render(request, 'register.html', context)

        # Create and activate user
        user = User.objects.create(username=un, email=em)
        user.set_password(p)  # Hash password
        user.is_active = True  # Activate user immediately
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("/login/")

    return render(request, "register.html")

# User Login
def ulogin(request):
    context = {}

    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["password"]

        if username == "" or password == "":
            context["error_msg"] = "All fields are required!"
            return render(request, "login.html", context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("/")  # Redirect to homepage
        else:
            context["error_msg"] = "Invalid username or password!"
            return render(request, "login.html", context)

    return render(request, "login.html")

# User Logout
def ulogout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("/login/")


def home_page(request):
    blogs = BlogPost.objects.all().order_by("-created_at")[:6]  
    return render(request, "home.html", {"blogs": blogs})


def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")  

        if not title or not content:
            return render(request, "create_blog.html", {"error": "Title and Content are required"})

        # Save the blog post
        blog = BlogPost(title=title, content=content, image=image, author=request.user)
        blog.save()

        return redirect("blog_list")  
    
    return render(request, "create_blog.html")


def blog_detail(request, blog_id):
    blog = BlogPost.objects.filter(id=blog_id).first()  

    if not blog:  
        return render(request, "blog_detail.html", {"error": "Blog not found!"})

    return render(request, "blog_detail.html", {"blog": blog})



def blog_list(request):
    blogs = BlogPost.objects.all().order_by("-created_at")  
    return render(request, "blog_list.html", {"blogs": blogs})


@login_required
def delete_blog(request, blog_id):
    blog = BlogPost.objects.filter(id=blog_id, author=request.user).first()  

    if blog:  
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
    else:
        messages.error(request, "You are not authorized to delete this blog or it does not exist.")

    return redirect('blog_list') 