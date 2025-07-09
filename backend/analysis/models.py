from django.db import models

class AnalysisResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    cilia_count = models.IntegerField()
    coloc_score = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image.name} - {self.cilia_count} cilia"
