from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Problemas, Submissions, TestCases, SubmissionTestCaseResult
from .serializers import CodeExecutionSerializer, ProblemSerializer, SubmissionSerializer, TestCaseSerializer
from .services.judge0 import submit_code, get_submission

class PruebaCodigo(APIView):
    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source_code = serializer.validated_data['source_code']
        language_id = serializer.validated_data['language_id']
        problema_id = serializer.validated_data['problema_id']
        user_id = request.data.get('user_id')  # o extraído desde request.headers o JWT

        try:
            problema = Problemas.objects.get(pk=problema_id)
        except Problemas.DoesNotExist:
            return Response({"error": "No se encontró el problema"}, status=status.HTTP_404_NOT_FOUND)

        testcases = problema.testcases.all()
        if not testcases.exists():
            return Response({"error": "No hay testcases"}, status=status.HTTP_400_BAD_REQUEST)

        all_passed = True
        first_output = ""
        error_output = None
        execution_time = None
        memory = None

        submission = Submissions.objects.create(
            user_id=user_id,
            problema=problema,
            source_code=source_code,
            language_id=language_id,
            stdin="",
            status="PENDING"
        )

        for i, testcase in enumerate(testcases):
            submission_data = submit_code(source_code, language_id, testcase.input_data)
            token = submission_data.get("token")
            result = get_submission(token)

            output = (result.get("stdout") or "").strip()
            expected = testcase.expected_output.strip()
            error = result.get("stderr") or result.get("compile_output")
            passed = (output == expected) and not error

            if i == 0:
                first_output = output
                error_output = error
                execution_time = result.get("time")
                memory = result.get("memory")

            SubmissionTestCaseResult.objects.create(
                submission=submission,
                input_data=testcase.input_data,
                expected_output=expected,
                user_output=output,
                passed=passed,
                error=error.strip() if error else None
            )

            if not passed:
                all_passed = False

        submission.status = "CORRECT" if all_passed else ("ERROR" if error_output else "WRONG")
        submission.output = first_output
        submission.error_output = error_output
        submission.execution_time = execution_time
        submission.memory = memory
        submission.save()

        results = submission.testcase_results.values(
            "input_data", "expected_output", "user_output", "passed", "error"
        )

        return Response({
            "submission_id": submission.id,
            "status": submission.status,
            "execution_time": execution_time,
            "memory": memory,
            "testcase_results": list(results)
        }, status=status.HTTP_200_OK)

##VISTAS PROBLEMAS
class CrearListarProblemas(generics.ListCreateAPIView):
    queryset = Problemas.objects.all().order_by('-creacion')
    serializer_class = ProblemSerializer

class EliminarProblema(APIView):
    def delete(self, request, id):
        try:
            problema = Problemas.objects.get(id=id)
            problema.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Problemas.DoesNotExist:
            return Response(
                {"error": "Problema no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class ActualizarProblema(APIView):
    serializer_class = ProblemSerializer
    def put(self, request, id, format=None):
        try:
            problema = Problemas.objects.get(id=id)
            serializer = ProblemSerializer(problema, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Problemas.DoesNotExist:
            return Response(
                {"error": "Problema no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

class ListaEnvios(generics.ListAPIView):
    queryset = Submissions.objects.all().order_by('-creacion')
    serializer_class = SubmissionSerializer

##VISTAS TESTCASES

class ListaTestCases(generics.ListAPIView):
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        problema_id = self.kwargs['id']
        return TestCases.objects.filter(problema_id=problema_id)

class CrearTestCase(generics.CreateAPIView):
    queryset = TestCases.objects.all()
    serializer_class = TestCaseSerializer

class EliminarTestCase(APIView):
    def delete(self, request, id):
        try:
            testCase = TestCases.objects.get(id=id)
            testCase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TestCases.DoesNotExist:
            return Response(
                {"error": "TestCase no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

class ActualizarTestCase(APIView):
    serializer_class = TestCaseSerializer
    def put(self, request, id, format=None):
        try:
            problema = TestCases.objects.get(id=id)
            serializer = TestCaseSerializer(problema, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except TestCases.DoesNotExist:
            return Response(
                {"error": "TestCase no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class CrearMultiplesTestCases(APIView):
    def post(self, request):
        test_cases = request.data.get('test_cases', [])
        problema_id = request.data.get('problema_id')

        if not test_cases or not problema_id:
            return Response({"error": "Faltan test cases o problema_id"}, status=status.HTTP_400_BAD_REQUEST)

        creados = []
        for tc_data in test_cases:
            tc_data['problema'] = problema_id  # Asociar el problema
            serializer = TestCaseSerializer(data=tc_data)
            if serializer.is_valid():
                serializer.save()
                creados.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(creados, status=status.HTTP_201_CREATED)