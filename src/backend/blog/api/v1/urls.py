from django.urls import path

from .views import (
    BlogListApiView,
    BlogCreateApiView,
    BlogUpdatedAPiView,
    BlogUpdatedStatusApiView,
    BlogDetailApiView
)

app_name = 'blog'

urlpatterns = [
    path('', BlogListApiView.as_view(), name='blog-list'),
    path('create/', BlogCreateApiView.as_view(), name='blog-create'),
    path(
        '<int:pk>/',
        BlogUpdatedAPiView.as_view(),
        name='blog-detail-update-delete',
    ),
    path(
        '<int:pk>/status/',
        BlogUpdatedStatusApiView.as_view(),
        name='blog-status-update',
    ),
    path("detail/<int:pk>/", BlogDetailApiView.as_view(), name="blog-detail"),
]