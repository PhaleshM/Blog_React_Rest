from http.client import responses
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions, AllowAny
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user

class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    
    queryset=Post.postobjects.all()
    # def get_queryset(self):
    #     user=self.request.user
    #     return Post.objects.filter(author=user)
    
class PostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)
    
class PostListDetailfilter(generics.ListAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    filter_backends=[filters.SearchFilter]
    search_fields = ['^slug']

    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    # '$' Regex search.

# Post Admin

# class CreatePost(generics.CreateAPIView):
#     permission_classes=[]
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

class CreatePost(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser, FormParser]

    def post(self,request, format=None):
        print(request.data)
        serializer= PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostDetal(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()
    serializer_class=PostSerializer

class EditPost(generics.UpdateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()
    serializer_class=PostSerializer

class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()
    serializer_class=PostSerializer

# class PostList(viewsets.ModelViewSet):
#     permission_classes=[PostUserWritePermission]
#     serializer_class=PostSerializer
#     # queryset=Post.postobjects.all()

#     def get_object(self,queryset=None,**kwargs):
#         item=self.kwargs.get('pk')
#         return get_object_or_404(Post,slug=item)
#     

#     def get_queryset(self):
#         user=self.request.user
#         return Post.objects.filter(author=user)
    
# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()

#     def list(self, request):
#         serializer_class=PostSerializer(self.queryset,many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request,pk=None):
#         post=get_object_or_404(self.queryset,pk=pk)
#         serializer_class=PostSerializer(post)
#         return Response(serializer_class.data)

    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass



""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
