from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core import paginator

from .models import User, Posting

class CreatePostingForm(ModelForm):
    class Meta:
        model = Posting
        fields = ['description', 'username']

    def __init__(self, *args, **kwargs):
        super(CreatePostingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

def index(request):
    # paginator = Paginator(postings, 1) use paginator to limit post #
    postings = Posting.objects.order_by("-creation_time").all()
    return render(request, "network/index.html", {
        "postings": postings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
# create post
@login_required
def create(request):
    if request.method == "POST":
        p = Posting(
            description = request.POST["description"],
            username = request.user
        )
        p.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index", {
            "form": CreatePostingForm()
        })

# user profile
@login_required
def profile(request, username):
    # username = username.object.get(username=username)
    profile = User.objects.get(username=username)
    return render(request, "network/profile.html", {
        "profile": profile
    })
    
#follow_add
@login_required
def following_add(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        user.followers.add(request.user)
        print("success")
        # add if statement for if self can't follow
        return HttpResponseRedirect(reverse("profile", args=(username,)))

# follow list
@login_required
def following(request):
    postings = Posting.objects.filter(username__in=request.user.followers.all()).order_by("-creation_time").all()
    return render(request, "network/following.html", {
        "postings": postings
        # "postings": ("followers", postings)
        # show_posts("followers", request, postings) 
    })

#following 
# @login_required
#     def following(request):
#         posts = Post.objects.filter(poster__in=request.user.following.all()).order_by("-creation_time").all()
#         return show_posts("Following", request, posts) 


#elijah follow_add
# @login_required
# def follow(request, username):
#     if request.method == "POST":
#         try:user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise Http404("User does not exist.") 
#         if user != request.user:user.followers.add(request.user)
# return HttpResponseRedirect(reverse("user", args=(username,)))

# unfollow someone

# @login_required
# def unfollow(request, username):
#     if request.method == "POST":
#         try:user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise Http404("User does not exist.")
#         if user != request.user:user.followers.remove(request.user)
# return HttpResponseRedirect(reverse("user", args=(username,)))

#following 
# @login_required
#     def following(request):
#         posts = Post.objects.filter(poster__in=request.user.following.all()).order_by("-creation_time").all()
#         return show_posts("Following", request, posts) 