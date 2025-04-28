from django.db import models

class Problemas(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    input_descripcion = models.TextField()
    output_descripcion = models.TextField()
    ejemplo_input = models.TextField()
    ejemplo_output = models.TextField()
    expected_output = models.TextField()
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Submissions(models.Model):
    STATUS_CHOICES = [
        ("CORRECT", "Correct"),
        ("WRONG", "Wrong Answer"),
    ]

    problema = models.ForeignKey(Problemas, on_delete=models.CASCADE, related_name='submissions')
    source_code = models.TextField()
    language_id = models.IntegerField()
    stdin = models.TextField(blank=True, default="")
    output = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
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

