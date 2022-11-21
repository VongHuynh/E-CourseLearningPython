from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer
from .paginator import BasePaginator
from rest_framework.decorators import action
from rest_framework.response import Response

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
