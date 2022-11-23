from django.urls import path, include
from rest_framework import routers
from . import views

# routers
router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet, 'category')
router.register("course", views.CourseViewSet, 'course')
router.register("lessons", views.LessonViewSet, 'lessons')
router.register("users", views.UserViewSet, 'users')
router.register("comments", views.CommentViewSet, 'comments')


#urls
urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]