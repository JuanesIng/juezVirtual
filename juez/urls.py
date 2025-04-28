from django.urls import path
from .views import PruebaCodigo, CrearListarProblemas, ListaEnvios, CrearTestCase

urlpatterns = [
    path('problemas/', CrearListarProblemas.as_view(), name='problem-list-create'),
    path('submissions/', ListaEnvios.as_view(), name='submission-list'),
    path('testcases/', CrearTestCase.as_view(), name='create-testcase'),
    path('run/', PruebaCodigo.as_view(), name='code-execute'),
]
