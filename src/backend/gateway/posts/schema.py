import graphene
from django.shortcuts import get_object_or_404
from graphql_jwt.decorators import login_required
from users.models import User

from .models import Comment, Follow, LikeComment, LikePost, Post
from .types import CommentType, FollowType, LikeCommentType, LikePostType, PostType


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    like_posts = graphene.List(LikePostType)
    like_comments = graphene.List(LikeCommentType)
    follows = graphene.List(FollowType)

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_comments(self, info):
        return Comment.objects.all()

    def resolve_like_posts(self, info):
        return LikePost.objects.all()

    def resolve_like_comments(self, info):
        return LikeComment.objects.all()

    def resolve_follows(self, info):
        return Follow.objects.all()


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, title, content):
        user = info.context.user  # Retrieve the user from the context
        post = Post(title=title, content=content, user=user)  # Add the user to the Post
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, post_id, title, content):
        user = info.context.user  # Retrieve the user from the context
        post = Post.objects.filter(post_id=post_id, user=user).first()

        if post:
            post.title = title
            post.content = content
            post.save()
            return UpdatePost(post=post)

        raise Exception("You are not authorized to update this post")


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    ok = graphene.String()

    def mutate(self, info, post_id):
        user = info.context.user  # Retrieve the user from the context
        post = Post.objects.filter(id=post_id, user=user).first()

        if post:
            post.delete()

        raise Exception("You are not authorized to delete this post")


class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, post_id, content):
        user = info.context.user  # Retrieve the user from the context
        post = get_object_or_404(Post, id=post_id)
        comment = Comment(post=post, content=content, author=user)  # Add the user as the author of the Comment
        comment.save()
        return CreateComment(comment=comment)


class UpdateComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, comment_id, content):
        user = info.context.user  # Retrieve the user from the context
        comment = Comment.objects.filter(id=comment_id, author=user).first()

        if comment:
            comment.content = content
            comment.save()
            return UpdateComment(comment=comment)

        raise Exception("You are not authorized to update this comment")


class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    ok = graphene.String()

    def mutate(self, info, comment_id):
        user = info.context.user  # Retrieve the user from the context
        comment = Comment.objects.filter(id=comment_id, author=user).first()

        if comment:
            comment.delete()
            return DeleteComment(ok="Comment deleted successfully")

        raise Exception("You are not authorized to delete this comment")


class ToggleFollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    follow = graphene.Field(FollowType)
    ok = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id):
        user = info.context.user
        following = get_object_or_404(User, id=user_id)
        follow, created = Follow.objects.get_or_create(follower=user, following=following)
        if not created:
            follow.delete()
            return ToggleFollowUser(follow=follow, ok="Unfollowed successfully")
        return ToggleFollowUser(follow=follow, ok="Followed successfully")


class ToggleLikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    like_post = graphene.Field(LikePostType)
    ok = graphene.String()

    @classmethod
    def mutate(cls, root, info, post_id):
        user = info.context.user
        post = Post.objects.get(id=post_id)
        like, created = LikePost.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return ToggleLikePost(like=like, ok="Post unliked successfully")
        return ToggleLikePost(like_post=like, ok="Post liked successfully")


class ToggleLikeComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    like_comment = graphene.Field(LikeCommentType)
    ok = graphene.String()

    @classmethod
    def mutate(cls, root, info, comment_id):
        user = info.context.user
        comment = Comment.objects.get(id=comment_id)
        like, created = LikeComment.objects.get_or_create(user=user, comment=comment)
        if not created:
            like.delete()
            return ToggleLikeComment(like_comment=like, ok="Comment unliked successfully")
        return ToggleLikeComment(like_comment=like, ok="Comment liked successfully")


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
    follow = ToggleFollowUser.Field()
    like_post = ToggleLikePost.Field()
    like_comment = ToggleLikeComment.Field()
