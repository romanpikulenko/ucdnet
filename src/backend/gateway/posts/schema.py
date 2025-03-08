import graphene
from django.shortcuts import get_object_or_404
from graphql_jwt.decorators import login_required
from users.models import User

from .models import Comment, Follow, LikeComment, LikePost, Post, PostMedia
from .types import CommentType, FollowType, LikeCommentType, LikePostType, PostType, PostMediaType


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post_media = graphene.List(PostMediaType)
    comments = graphene.List(CommentType)
    like_posts = graphene.List(LikePostType)
    like_comments = graphene.List(LikeCommentType)
    follows = graphene.List(FollowType)

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post_media(self, info):
        return PostMedia.objects.all()

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
    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, title, content):
        user = info.context.user  # Retrieve the user from the context
        post = Post(title=title, content=content, user=user)  # Add the user to the Post
        post.save()
        return CreatePost(post=post, ok="Post created successfully")


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)
    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, post_id, title, content):
        user = info.context.user  # Retrieve the user from the context
        post = Post.objects.filter(post_id=post_id, user=user).first()

        if post:
            post.title = title
            post.content = content
            post.save()
            return UpdatePost(post=post, ok="Post updated successfully")

        return UpdatePost(post=None, ok="Post not found")


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, post_id):
        user = info.context.user  # Retrieve the user from the context
        post = Post.objects.filter(id=post_id, user=user).first()

        if post:
            post.delete()
            return DeletePost(ok="Post deleted successfully")

        return DeletePost(ok="Post not found")


# Delete PostMedia mutation use post_id and order to find out needed PostMedia
class DeletePostMedia(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        order = graphene.Int(required=True)

    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, post_id, order):
        user = info.context.user
        post = Post.objects.filter(id=post_id, user=user).first()

        if post:
            post_media = PostMedia.objects.filter(post=post, order=order).first()
            if post_media:
                post_media.delete()
                return DeletePostMedia(ok="PostMedia deleted successfully")
            else:
                return DeletePostMedia(ok="PostMedia not found")

        return DeletePostMedia(ok="Post not found")


class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, post_id, content):
        user = info.context.user  # Retrieve the user from the context
        post = get_object_or_404(Post, id=post_id)
        comment = Comment(post=post, content=content, author=user)  # Add the user as the author of the Comment
        comment.save()
        return CreateComment(comment=comment, ok="Comment created successfully")


class UpdateComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, comment_id, content):
        user = info.context.user  # Retrieve the user from the context
        comment = Comment.objects.filter(id=comment_id, author=user).first()

        if comment:
            comment.content = content
            comment.save()
            return UpdateComment(comment=comment, ok="Comment updated successfully")

        raise UpdateComment(comment=None, ok="Comment not found")


class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    ok = graphene.String()

    @login_required  # Ensure the user is authenticated
    def mutate(self, info, comment_id):
        user = info.context.user  # Retrieve the user from the context
        comment = Comment.objects.filter(id=comment_id, author=user).first()

        if comment:
            comment.delete()
            return DeleteComment(ok="Comment deleted successfully")

        raise DeleteComment(ok="Comment not found")


class ToggleFollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    follow = graphene.Field(FollowType)
    ok = graphene.String()

    @classmethod
    @login_required  # Ensure the user is authenticated
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
        reaction = graphene.String(required=False)

    like_post = graphene.Field(LikePostType)
    ok = graphene.String()

    @classmethod
    @login_required  # Ensure the user is authenticated
    def mutate(cls, root, info, post_id):
        user = info.context.user
        post = get_object_or_404(Post, id=post_id)
        reaction = info.context.GET.get("reaction")
        liked_post = LikePost.objects.filter(user=user, post=post).first()

        if not liked_post:
            reaction = reaction or "like"
            LikePost.objects.create(user=user, post=post, reaction=reaction)
            return ToggleLikePost(like_post=liked_post, ok="Post liked successfully")

        if reaction:
            liked_post.reaction = reaction
            liked_post.save()
            return ToggleLikePost(like_post=liked_post, ok="Post reaction updated successfully")
        else:
            liked_post.delete()
            return ToggleLikePost(like_post=None, ok="Post unliked successfully")


class ToggleLikeComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)
        reaction = graphene.String(required=False)

    like_comment = graphene.Field(LikeCommentType)
    ok = graphene.String()

    @classmethod
    @login_required  # Ensure the user is authenticated
    def mutate(cls, root, info, comment_id):
        user = info.context.user
        comment = get_object_or_404(Comment, id=comment_id)
        reaction = info.context.GET.get("reaction")
        liked_comment = LikeComment.objects.filter(user=user, comment=comment).first()

        if not liked_comment:
            reaction = reaction or "like"
            LikeComment.objects.create(user=user, comment=comment, reaction=reaction)
            return ToggleLikeComment(like_comment=liked_comment, ok="Comment liked successfully")

        if reaction:
            liked_comment.reaction = reaction
            liked_comment.save()
            return ToggleLikeComment(like_comment=liked_comment, ok="Comment reaction updated successfully")
        else:
            liked_comment.delete()
            return ToggleLikeComment(like_comment=None, ok="Comment unliked successfully")


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
