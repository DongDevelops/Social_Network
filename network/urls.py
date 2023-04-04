
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follwings_posts/<int:user_id>", views.follwings_posts, name="follwings_posts"),


    #API ROUTES
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("delete/<int:post_id>", views.delete, name="delete"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("add_comment/<int:post_id>", views.add_comment, name="add_comment"),
    path("delete_comment/<int:post_id>", views.delete_comment, name="delete_comment")
]
