from django.urls import path, include
from rest_framework import routers
from . import views

# routers
router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet, 'category')
router.register("course", views.CourseViewSet, 'course')

#urls
urlpatterns = [
    path('', include(router.urls)),
]