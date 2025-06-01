from django.urls import path
from .views import PruebaCodigo, CrearListarProblemas, ListaEnvios, CrearTestCase, EliminarProblema, ActualizarProblema, EliminarTestCase, ActualizarTestCase, ListaTestCases


urlpatterns = [
    path('problemas/', CrearListarProblemas.as_view(), name='listar-crear-problema'),
    path('problemas/eliminar/<int:id>/', EliminarProblema.as_view(), name='eliminar-problema'),
    path('problemas/editar/<int:id>/', ActualizarProblema.as_view(), name='ctualizar-problema'),
    path('submissions/', ListaEnvios.as_view(), name='listar-submission'),
    path('testcases/', CrearTestCase.as_view(), name='crear-testcase'),
    path('problemas/<int:id>/testcases', ListaTestCases.as_view(), name='crear-testcase'),
    path('testcases/eliminar/<int:id>/', EliminarTestCase.as_view(), name='eliminar-testcase'),
    path('testcases/editar/<int:id>/', ActualizarTestCase.as_view(), name='actualizar-testcase'),
    path('run/', PruebaCodigo.as_view(), name='ejecutor'),
]
