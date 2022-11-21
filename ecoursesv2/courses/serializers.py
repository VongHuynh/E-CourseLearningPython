from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Course, Lesson

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, course):
        request = self.context['request']
        name = course.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path) # user build_absolute_uri to get domain
    class Meta:
        model = Course
        fields = ["id", "subject", "image", "created_date", "category"]

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "subject", "image", "created_date", 
        "updated_date", "course"]