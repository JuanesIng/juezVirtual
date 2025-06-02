from django.db import models


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("Fácil", "Fácil"),
        ("Media", "Media"),
        ("Difícil", "Difícil"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    example_input = models.TextField()
    example_output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="Media")

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class Submission(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CORRECT", "Correct"),
        ("WRONG", "Wrong Answer"),
        ("ERROR", "Runtime/Error"),
        ("TIMEOUT", "Time Limit Exceeded"),
    ]

    user_id = models.CharField(max_length=100, null=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    source_code = models.TextField()
    language_id = models.IntegerField()
    stdin = models.TextField(blank=True, default="")
    output = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    execution_time = models.CharField(max_length=20, blank=True, null=True)
    memory_usage = models.CharField(max_length=20, blank=True, null=True)
    error_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} - {self.problem.title}"


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        visibility = "Visible" if self.is_visible else "Hidden"
        return f"Caso de prueba para {self.problem.title} ({visibility})"


class SubmissionTestCaseResult(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='test_case_results')
    input_data = models.TextField()
    expected_output = models.TextField()
    user_output = models.TextField(blank=True, null=True)
    passed = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        result = "Passed" if self.passed else "Failed"
        return f"Resultado de caso de prueba para envío {self.submission.id} - {result}"
