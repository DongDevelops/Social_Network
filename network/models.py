from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "followers": len(self.follower_people.all())
        }


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    follower_people = models.ManyToManyField(User, blank=True, related_name="follower_people")


class Followings(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_people = models.ManyToManyField(User, blank=True, related_name="following_people")


class Posts(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "likes": len(self.like_post.all()),
            "comments_amount": len(self.commented_post.all())
        }

class LikeUnlike(models.Model):
    like_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    like_post = models.ManyToManyField(Posts, blank=True, related_name="like_post")

class Comments(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=64)
    commented_post = models.ManyToManyField(Posts, blank=True, related_name="commented_post")

    def serialize(self):
        return {
            "id": self.id,
            "commentor": self.commentor.username,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "comment": self.comment
        }