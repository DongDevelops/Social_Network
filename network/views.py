import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Posts, Followings, Followers, LikeUnlike, Comments


@csrf_exempt
def index(request):
    if request.method == "POST":
        content = request.POST["text"]
        user = request.user
        time = datetime.now()
        new_post = Posts.objects.create(poster=user, content=content, time=time)
        new_post.save()
        posts = Posts.objects.all()
        ordered_posts = posts.order_by("-time").all()

        paginator = Paginator(ordered_posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj
        })

    else:
        posts = Posts.objects.all()
        ordered_posts = posts.order_by("-time").all()

        paginator = Paginator(ordered_posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj
        })


def profile(request, user_id):
    user1 = User.objects.get(id=user_id)
    all_posts = Posts.objects.filter(poster=user1)

    ordered_posts = sorted(all_posts, key=lambda item: item.time, reverse=True)
    paginator = Paginator(ordered_posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "user1": user1
    })


@csrf_exempt
def follow(request, user_id):
    if request.method == "GET":

        user = User.objects.get(id=user_id)
        user2_id = request.user.id
        user2 = User.objects.get(id=user2_id)
        user_follower_people = user.follower_people.all()
        user2_following_people = user2.following_people.all()

        count = 0
        for i in user_follower_people:
            for j in user2_following_people:
                if i.follower == user2 and j.following == user:
                    user.follower_people.remove(i)
                    user.save()
                    user2.following_people.remove(j)
                    user2.save()
                    count = count + 1
                    break
                else:
                    pass

        if count == 0:
            new_follower = Followers.objects.create(follower=user2)
            new_following = Followings.objects.create(following=user)
            user.follower_people.add(new_follower)
            user2.following_people.add(new_following)
            user.save()
            user2.save()
        else:
            pass
        return JsonResponse(user.serialize())

    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


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


@csrf_exempt
def edit(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return JsonResponse(post.serialize())

    elif request.method == "GET":
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def follwings_posts(request, user_id):
    user = User.objects.get(id=user_id)
    following_users = user.following_people.all()


    new_list = []
    for following_user in following_users:
        final = following_user.following
        all_posts = Posts.objects.filter(poster=final)
        new_list.extend(all_posts)


    ordered_posts = sorted(new_list, key=lambda item: item.time, reverse=True)
    paginator = Paginator(ordered_posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })



@csrf_exempt
@login_required
def likes(request, post_id):
    try:
        user = request.user
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        all_likes = post.like_post.all()
        count = 0
        for like in all_likes:
            already_liked_user = like.like_user
            if (already_liked_user == user):
                post.like_post.remove(like)
                count = count + 1
                post.save()
                break
            else:
                pass
        if (count == 0):
            new_like = LikeUnlike.objects.create(like_user=user)
            post.like_post.add(new_like)
            post.save()
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
def add_comment(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            b = data["content"]
            now = datetime.now()
            user = request.user
            current_time = now.strftime("%H:%M:%S")
            new_comment = Comments.objects.create(commentor=user, time=current_time, comment=b)
            new_comment.save()
            post.commented_post.add(new_comment)
            post.save()
        return JsonResponse(new_comment.serialize())

    elif request.method == "GET":
        return JsonResponse(post.serialize())
    
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
def delete_comment(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            comment_id = data["content"]
            comment = Comments.objects.get(id=comment_id)
            post.commented_post.remove(comment)
            post.save()
            Comments.objects.filter(id=comment_id).delete()
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def delete(request, post_id):
    if request.method == "GET":
        Posts.objects.filter(id=post_id).delete()
        return HttpResponse(status=204)
