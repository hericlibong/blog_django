from django.urls import path

from .views import (
    PostCreateSuccessView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("create/success/", PostCreateSuccessView.as_view(), name="post_create_success"),
    path("update/<slug:slug>/", PostUpdateView.as_view(), name="post_update"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("delete/<slug:slug>/", PostDeleteView.as_view(), name="post_delete"),
]
