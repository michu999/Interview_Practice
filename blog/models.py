from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.conf import settings


class AIPrompt(models.Model):
    """Model for storing AI prompts used to generate blog posts"""
    AI_MODEL_CHOICES = [
        ('ChatGPT', 'ChatGPT'),
        ('Gemini', 'Gemini'),
        ('DeepSeek', 'DeepSeek'),
    ]

    model_name = models.CharField(max_length=50, choices=AI_MODEL_CHOICES)
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_prompts'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.model_name} - {self.prompt_text[:50]}... ({self.created_at.strftime('%Y-%m-%d')})"


class Post(models.Model):
    """Blog post model for AI-generated travel content"""
    AI_MODEL_CHOICES = [
        ('ChatGPT', 'ChatGPT'),
        ('Gemini', 'Gemini'),
        ('DeepSeek', 'DeepSeek'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50, choices=AI_MODEL_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ai_prompt = models.ForeignKey(
        AIPrompt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_posts',
        help_text='AI prompt used to generate this post'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - by {self.author}"

    @property
    def average_rating(self):
        """Calculate average rating dynamically"""
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg is not None else None

    @property
    def rating_count(self):
        """Get total number of ratings"""
        return self.ratings.count()


class Rating(models.Model):
    """Rating model for user ratings on posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating {self.score}/10 for {self.post.title}"

