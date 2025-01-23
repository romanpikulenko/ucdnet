# File: schema_relay.py
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import Comment, Post


# Define the PostType and CommentType with the Node interface
class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "title": ["exact", "icontains", "istartswith"],
            "content": ["exact", "icontains", "istartswith"],
            "user": ["exact"],
            "created_at": ["exact", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "gt", "gte", "lt", "lte"],
        }


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "content": ["exact", "icontains", "istartswith"],
            "author": ["exact"],
            "post": ["exact"],
            "created_at": ["exact", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "gt", "gte", "lt", "lte"],
        }


# Define the Query with relay connection fields
class Query(graphene.ObjectType):
    post = graphene.relay.Node.Field(PostNode)
    comment = graphene.relay.Node.Field(CommentNode)
    all_posts = DjangoFilterConnectionField(PostNode)
    all_comments = DjangoFilterConnectionField(CommentNode)
