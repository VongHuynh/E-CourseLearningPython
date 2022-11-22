from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, serializers
from .models import Category, Course, Lesson, Tag, User
from .serializers import (CategorySerializer,
                          CourseSerializer,
                          LessonSerializer,
                          TagSerializer,
                          LessonDetailSerialize,
                          UserSerializer)
from .paginator import BasePaginator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
from drf_spectacular.utils import extend_schema

# Create your views here.


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        courses = Course.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            courses = courses.filter(subject__icontains=q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses = courses.filter(category_id=cate_id)

        return courses

    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lesson(self, request, pk):
        course = Course.objects.get(pk=pk)
        lessons = course.lessons.filter(active=True)

        kw = request.query_params.get('kw')
        if kw is not None:
            lessons = lessons.filter(subject__icontains=kw)

        return Response(LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerialize

    @action(methods=['post'], detail=True, url_path="tags")
    def add_Tag(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)
                lesson.save()
                return Response(self.serializer_class(lesson).data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "get_current_user":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    @action(methods=['GET'], detail=False, url_path="current-users")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
        status=status.HTTP_200_OK)

# class EmptyPayloadResponseSerializer(serializers.Serializer):
#     detail = serializers.CharField()
class AuthInfo(APIView):
    #@extend_schema(request=None, responses=EmptyPayloadResponseSerializer)
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

