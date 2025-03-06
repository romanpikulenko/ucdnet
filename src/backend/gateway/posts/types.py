from graphene_django import DjangoObjectType
from .models import Post, PostMedia, Comment, LikePost, LikeComment, Follow


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        # interfaces = (graphene.relay.Node,)


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        # interfaces = (graphene.relay.Node,)


class LikePostType(DjangoObjectType):
    class Meta:
        model = LikePost
        # interfaces = (graphene.relay.Node,)


class LikeCommentType(DjangoObjectType):
    class Meta:
        model = LikeComment
        # interfaces = (graphene.relay.Node,)


class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        # interfaces = (graphene.relay.Node,)


class PostMediaType(DjangoObjectType):
    class Meta:
        model = PostMedia
        # interfaces = (graphene.relay.Node,)
