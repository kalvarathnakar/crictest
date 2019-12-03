from rest_framework import serializers
from accounts.models import *


class UpdateSubjectDetailsSerializer(serializers.Serializer):
	subject_id_list = serializers.ListField()