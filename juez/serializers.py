from rest_framework import serializers
from .models import Problem, Submission, TestCase


class CodeExecutionSerializer(serializers.Serializer):
    source_code = serializers.CharField()
    language_id = serializers.IntegerField()
    problem_id = serializers.IntegerField()

    def validate(self, data):
        if not data.get('source_code'):
            raise serializers.ValidationError("Source code is required.")
        if not data.get('language_id'):
            raise serializers.ValidationError("Language ID is required.")
        if not data.get('problem_id'):
            raise serializers.ValidationError("Problem ID is required.")
        return data


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id',
            'user_id',
            'problem',
            'source_code',
            'language_id',
            'stdin',
            'output',
            'status',
            'execution_time',
            'memory_usage',
            'error_output',
            'created_at'
        ]


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            'id',
            'problem',
            'input_data',
            'expected_output',
            'is_visible',
            'created_at'
        ]


class ProblemSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'description',
            'input_description',
            'output_description',
            'example_input',
            'example_output',
            'difficulty',
            'created_at',
            'test_cases'
        ]
