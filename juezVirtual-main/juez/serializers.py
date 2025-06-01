from rest_framework import serializers
from .models import Problemas, Submissions, TestCases

class CodeExecutionSerializer(serializers.Serializer):
    source_code = serializers.CharField()
    language_id = serializers.IntegerField()
    problema_id = serializers.IntegerField()


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = "__all__"

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = "__all__"

class ProblemSerializer(serializers.ModelSerializer):
    testcases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Problemas
        fields = "__all__"

