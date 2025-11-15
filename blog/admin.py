from django.contrib import admin
from .models import Post, Rating, AIPrompt


@admin.register(AIPrompt)
class AIPromptAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'get_prompt_preview', 'created_by', 'created_at', 'get_generated_posts_count']
    list_filter = ['model_name', 'created_at', 'created_by']
    search_fields = ['prompt_text', 'model_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

    def get_prompt_preview(self, obj):
        return obj.prompt_text[:100] + '...' if len(obj.prompt_text) > 100 else obj.prompt_text
    get_prompt_preview.short_description = 'Prompt Preview'

    def get_generated_posts_count(self, obj):
        return obj.generated_posts.count()
    get_generated_posts_count.short_description = 'Generated Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'latitude', 'longitude', 'created_at', 'get_average_rating', 'is_ai_generated']
    list_filter = ['author', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    def get_average_rating(self, obj):
        return obj.average_rating if obj.average_rating else 'No ratings yet'
    get_average_rating.short_description = 'Avg Rating'

    def is_ai_generated(self, obj):
        return bool(obj.ai_prompt)
    is_ai_generated.short_description = 'AI Generated'
    is_ai_generated.boolean = True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['post', 'score', 'user_ip', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['post__title']
    date_hierarchy = 'created_at'
