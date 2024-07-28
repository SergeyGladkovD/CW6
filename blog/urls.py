from django.urls import path
from blog.apps import BlogConfig
from blog.views import (
    MaterialCreateView,
    MaterialListView,
    MaterialDetailView,
    MaterialUpdateView,
    MaterialDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("create/", MaterialCreateView.as_view(), name="create_blog"),
    path("", MaterialListView.as_view(), name="list_blog"),
    path("view/<int:pk>/", MaterialDetailView.as_view(), name="view_blog"),
    path("edit/<int:pk>", MaterialUpdateView.as_view(), name="edit_blog"),
    path("delete/<int:pk>", MaterialDeleteView.as_view(), name="delete_blog"),
]
