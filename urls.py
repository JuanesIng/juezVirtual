from django.urls import path
from .views import (
    PruebaCodigo,
    CrearListarProblemas,
    ListaCrearEnvios,
    EliminarProblema,
    ActualizarProblema,
    EliminarTestCase,
    ActualizarTestCase,
    ListaTestCases,
    CrearMultiplesTestCases,
)

urlpatterns = [
    path('problemas/', CrearListarProblemas.as_view(), name='listar-crear-problema'),
    path('problemas/eliminar/<int:id>/', EliminarProblema.as_view(), name='eliminar-problema'),
    path('problemas/editar/<int:id>/', ActualizarProblema.as_view(), name='actualizar-problema'),
    path('problemas/<int:id>/testcases', ListaTestCases.as_view(), name='listar-testcases'),

    path('submissions/', ListaCrearEnvios.as_view(), name='listar-submissions'),

    path('testcases/', CrearMultiplesTestCases.as_view(), name='crear-multiples-testcases'),
    path('testcases/eliminar/<int:id>/', EliminarTestCase.as_view(), name='eliminar-testcase'),
    path('testcases/editar/<int:id>/', ActualizarTestCase.as_view(), name='editar-testcase'),

    path('run/', PruebaCodigo.as_view(), name='ejecutar-codigo'),
]
