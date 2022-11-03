from .models import *
from rest_framework import serializers


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = "__all__"
