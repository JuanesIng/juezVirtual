from django.db import models

class Problemas(models.Model):
    DIFICULTAD_CHOICES = [
        ("Facil", "Fácil"),
        ("Media", "Media"),
        ("Dificil", "Difícil"),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    input_descripcion = models.TextField()
    output_descripcion = models.TextField()
    ejemplo_input = models.TextField()
    ejemplo_output = models.TextField()
    creacion = models.DateTimeField(auto_now_add=True)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default="Media")

    def __str__(self):
        return self.titulo


class Submissions(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CORRECT", "Correct"),
        ("WRONG", "Wrong Answer"),
        ("ERROR", "Runtime/Error"),
        ("TIMEOUT", "Time Limit Exceeded"),
    ]

    user_id = models.CharField(max_length=100, null=True, blank=True)
    problema = models.ForeignKey(Problemas, on_delete=models.CASCADE, related_name='submissions')
    source_code = models.TextField()
    language_id = models.IntegerField()
    stdin = models.TextField(blank=True, default="")
    output = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    execution_time = models.CharField(max_length=20, blank=True, null=True)
    memory = models.CharField(max_length=20, blank=True, null=True)
    error_output = models.TextField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} - {self.problema.titulo}"
    
class TestCases(models.Model):
    problema = models.ForeignKey(Problemas, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField()
    expected_output = models.TextField()
    visible = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TestCase para {self.problema.titulo}"

class SubmissionTestCaseResult(models.Model):
    submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name='testcase_results')
    input_data = models.TextField()
    expected_output = models.TextField()
    user_output = models.TextField(blank=True, null=True)
    passed = models.BooleanField(default=False)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resultado del test case para Submission {self.submission.id}"