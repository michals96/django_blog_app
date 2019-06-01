from django.urls import path

from wykop.posts.views import (CommentCreateView, PostCreate, PostDelete,
                               PostDetail, PostList, PostUpdate, TopPostList)

app_name = 'posts'

urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('new', PostCreate.as_view(), name='create'),
    path('<int:pk>', PostDetail.as_view(), name='detail'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='delete'),
    path('top/',TopPostList.as_view(), name='top-list'),
    path('comment/<int:post_pk>',CommentCreateView.as_view(), name='comment'),
]
