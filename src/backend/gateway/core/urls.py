from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        # Add urls from home.urls
        path("", include("home.urls")),
        # Add urls from users.urls
        path("users/", include("users.urls")),
        # Add urls from posts.urls
        path("posts/", include("posts.urls")),
        # Add graphql url
        path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
