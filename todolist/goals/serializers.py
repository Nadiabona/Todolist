from rest_framework import serializers
from todolist.goals.models import GoalCategory
from todolist.core.serializers import ProfileSerializer


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #в джанго в дефолт хидден юзер можно забирать только не в методаз put patch
    #'поле, которое не видит юзер, видим мы, чтобы удобно было работать с контекстом запроса

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    #в джанго в дефолт хидден юзер можно забирать только не в методаз put patch
    #'поле, которое не видит юзер, видим мы, чтобы удобно было работать с контекстом запроса

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"