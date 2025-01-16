from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        # Add graphql url
        path("graphql/", GraphQLView.as_view(graphiql=True)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
