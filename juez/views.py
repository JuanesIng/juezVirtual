from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Problem, Submission, TestCase, SubmissionTestCaseResult
from .serializers import (
    CodeExecutionSerializer,
    ProblemSerializer,
    SubmissionSerializer,
    TestCaseSerializer
)
from .services.judge0 import submit_code, get_submission


class CodeExecutionView(APIView):
    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source_code = serializer.validated_data['source_code']
        language_id = serializer.validated_data['language_id']
        problem_id = serializer.validated_data['problem_id']
        user_id = request.data.get('user_id')

        try:
            problem = Problem.objects.get(pk=problem_id)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)

        test_cases = problem.test_cases.all()
        if not test_cases.exists():
            return Response({"error": "No test cases found"}, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(
            user_id=user_id,
            problem=problem,
            source_code=source_code,
            language_id=language_id,
            stdin="",
            status="PENDING"
        )

        all_passed = True
        first_output = ""
        error_output = None
        execution_time = None
        memory_usage = None

        for idx, test_case in enumerate(test_cases):
            submission_data = submit_code(source_code, language_id, test_case.input_data)
            token = submission_data.get("token")
            result = get_submission(token)

            output = (result.get("stdout") or "").strip()
            expected_output = test_case.expected_output.strip()
            error = result.get("stderr") or result.get("compile_output")
            passed = (output == expected_output) and not error

            if idx == 0:
                first_output = output
                error_output = error
                execution_time = result.get("time")
                memory_usage = result.get("memory")

            SubmissionTestCaseResult.objects.create(
                submission=submission,
                input_data=test_case.input_data,
                expected_output=expected_output,
                user_output=output,
                passed=passed,
                error_message=error.strip() if error else None
            )

            if not passed:
                all_passed = False

        submission.status = "CORRECT" if all_passed else ("ERROR" if error_output else "WRONG")
        submission.output = first_output
        submission.error_output = error_output
        submission.execution_time = execution_time
        submission.memory_usage = memory_usage
        submission.save()

        results = submission.test_case_results.values(
            "input_data", "expected_output", "user_output", "passed", "error_message"
        )

        return Response({
            "submission_id": submission.id,
            "status": submission.status,
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "test_case_results": list(results)
        }, status=status.HTTP_200_OK)


# PROBLEM VIEWS

class ProblemListCreateView(generics.ListCreateAPIView):
    queryset = Problem.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer


class ProblemDeleteView(APIView):
    def delete(self, request, id):
        try:
            problem = Problem.objects.get(id=id)
            problem.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)


class ProblemUpdateView(APIView):
    def put(self, request, id):
        try:
            problem = Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProblemSerializer(problem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SUBMISSION VIEWS

class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all().order_by('-created_at')
    serializer_class = SubmissionSerializer


# TEST CASE VIEWS

class TestCaseCreateView(generics.CreateAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer


class TestCaseDeleteView(APIView):
    def delete(self, request, id):
        try:
            test_case = TestCase.objects.get(id=id)
            test_case.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TestCase.DoesNotExist:
            return Response({"error": "Test case not found"}, status=status.HTTP_404_NOT_FOUND)


class TestCaseUpdateView(APIView):
    def put(self, request, id):
        test_cases_data = request.data.get('test_cases', [])

        if not test_cases_data:
            return Response({"error": "No test cases provided"}, status=status.HTTP_400_BAD_REQUEST)

        TestCase.objects.filter(problem_id=id).delete()

        created_test_cases = []
        for tc_data in test_cases_data:
            tc_data['problem'] = id
            serializer = TestCaseSerializer(data=tc_data)
            if serializer.is_valid():
                serializer.save()
                created_test_cases.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_test_cases, status=status.HTTP_200_OK)


class TestCaseListView(generics.ListAPIView):
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        problem_id = self.kwargs['id']
        return TestCase.objects.filter(problem_id=problem_id)


class MultipleTestCaseCreateView(APIView):
    def post(self, request):
        test_cases_data = request.data.get('test_cases', [])
        problem_id = request.data.get('problem_id')

        if not test_cases_data or not problem_id:
            return Response({"error": "Missing test cases or problem_id"}, status=status.HTTP_400_BAD_REQUEST)

        created_test_cases = []
        for tc_data in test_cases_data:
            tc_data['problem'] = problem_id
            serializer = TestCaseSerializer(data=tc_data)
            if serializer.is_valid():
                serializer.save()
                created_test_cases.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_test_cases, status=status.HTTP_201_CREATED)
