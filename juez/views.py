from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Problemas, Submissions, TestCases
from .serializers import CodeExecutionSerializer, ProblemSerializer, SubmissionSerializer, TestCaseSerializer
from .services.judge0 import submit_code, get_submission

class PruebaCodigo(APIView):
    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        if serializer.is_valid():
            source_code = serializer.validated_data['source_code']
            language_id = serializer.validated_data['language_id']
            problema_id = request.data.get('problema_id')

            if not problema_id:
                return Response({"error": "Se requiere problem_id"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                problema = Problemas.objects.get(pk=problema_id)
                testcases = problema.testcases.all()

                if not testcases.exists():
                    return Response({"error": "No hay testcases"}, status=status.HTTP_400_BAD_REQUEST)

                all_passed = True
                testcase_results = []

                for testcase in testcases:
                    submission_data = submit_code(source_code, language_id, testcase.input_data)
                    token = submission_data.get("token")
                    result = get_submission(token)

                    output = result.get("stdout", "").strip()
                    expected = testcase.expected_output.strip()

                    pasado = (output == expected)

                    testcase_results.append({
                        "input": testcase.input_data,
                        "expected_output": expected,
                        "user_output": output,
                        "passed": pasado
                    })

                    if not pasado:
                        all_passed = False

                submission_status = "CORRECT" if all_passed else "WRONG"

                submission = Submissions.objects.create(
                    problema=problema,
                    source_code=source_code,
                    language_id=language_id,
                    stdin="",
                    output=testcase_results[-1]["user_output"] if testcase_results else "",
                    status=submission_status
                )

                return Response({
                    "submission_id": submission.id,
                    "status": submission.status,
                    "testcase_results": testcase_results
                }, status=status.HTTP_200_OK)

            except Problemas.DoesNotExist:
                return Response({"error": "No se encontró el problema"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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