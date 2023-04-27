from django.urls import path
from .views import PostList, PostDetail, PostListDetailfilter, CreatePost,EditPost,DeletePost,AdminPostDetal
from rest_framework.routers import DefaultRouter

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

app_name = 'blog_api'

# router= DefaultRouter()
# router.register('', PostList,basename='post')
# urlpatterns = router.urls


urlpatterns = [
    path('post/<str:pk>/', PostDetail.as_view(), name='detailcreate'),
    path('', PostList.as_view(), name='listcreate'),
    path('search/',PostListDetailfilter.as_view(),name='postsearch'),
    # Post Admin urls
    path('admin/create/',CreatePost.as_view(),name='craetepost'),
    path('admin/edit/postdetail/<int:pk>/',AdminPostDetal.as_view(),name='admindetailpost'),
    path('admin/edit/<int:pk>/',EditPost.as_view(),name='editpost'),
    path('admin/delete/<int:pk>/',DeletePost.as_view(),name='deletepost'),

]
