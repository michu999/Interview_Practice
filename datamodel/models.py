from django.db import models

# Create your models here.
class AIModelLog(models.Model):
    model_name = models.CharField(max_length=255)
    input_data = models.TextField()
    output_data = models.TextField()
    processing_time = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} - {self.input_data} : {self.output_data} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} : {self.processing_time}"