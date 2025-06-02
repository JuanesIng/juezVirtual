from django.urls import path
from .views import (
    CodeExecutionView,
    ProblemListCreateView,
    ProblemDeleteView,
    ProblemUpdateView,
    SubmissionListCreateView,
    TestCaseListView,
    TestCaseCreateView,
    TestCaseDeleteView,
    TestCaseUpdateView,
    MultipleTestCaseCreateView,
)

urlpatterns = [
    # Problems
    path('problems/', ProblemListCreateView.as_view(), name='problem-list-create'),
    path('problems/delete/<int:id>/', ProblemDeleteView.as_view(), name='problem-delete'),
    path('problems/update/<int:id>/', ProblemUpdateView.as_view(), name='problem-update'),
    path('problems/<int:id>/test-cases/', TestCaseListView.as_view(), name='testcase-list'),

    # Submissions
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list-create'),

    # Test Cases
    path('test-cases/', MultipleTestCaseCreateView.as_view(), name='testcase-multiple-create'),
    path('test-cases/delete/<int:id>/', TestCaseDeleteView.as_view(), name='testcase-delete'),
    path('test-cases/update/<int:id>/', TestCaseUpdateView.as_view(), name='testcase-update'),

    # Code Execution
    path('execute/', CodeExecutionView.as_view(), name='code-execution'),
]

