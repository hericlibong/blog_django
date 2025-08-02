from django.urls import path
from .views import (
    PostCreateView, PostCreateSuccessView,
    PostListView, PostUpdateView, PostDetailView,
    PostDeleteView, 
)
app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/success/', PostCreateSuccessView.as_view(), name='post_create_success'),
    path('update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
   # path('beautifull-f1/', BeautifulF1ListView.as_view(), name='beautifull_f1')

]
