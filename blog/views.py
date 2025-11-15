from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Post, Rating, AIPrompt
from .forms import AIPromptForm
from .ai_services import generate_ai_blog_post
import logging

# Configure logging
logger = logging.getLogger(__name__)


def post_list(request):
    """Homepage view displaying all posts with average ratings"""
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    """Detail view for a single post with map and rating form"""
    post = get_object_or_404(Post, pk=pk)
    recent_ratings = post.ratings.all()[:5]  # Show 5 most recent ratings

    context = {
        'post': post,
        'recent_ratings': recent_ratings,
    }
    return render(request, 'blog/post_detail.html', context)


@require_POST
def submit_rating(request, pk):
    """AJAX endpoint for submitting ratings"""
    post = get_object_or_404(Post, pk=pk)

    try:
        score = int(request.POST.get('score'))

        # Validate score
        if score < 1 or score > 10:
            return JsonResponse({
                'success': False,
                'error': 'Rating must be between 1 and 10'
            }, status=400)

        # Get user IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')

        # Create rating
        rating = Rating.objects.create(
            post=post,
            score=score,
            user_ip=user_ip
        )

        return JsonResponse({
            'success': True,
            'average_rating': post.average_rating,
            'rating_count': post.rating_count,
            'message': 'Rating submitted successfully!'
        })

    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid rating value'
        }, status=400)


# AI generation is now handled by the ai_services module


@staff_member_required
def add_ai_post(request):
    """
    View for creating AI-generated blog posts using real AI APIs
    Only accessible to staff/admin users

    Security: Requires user to be authenticated AND have staff privileges
    """
    # Double-check user permissions (defensive programming)
    if not request.user.is_authenticated:
        logger.warning(
            f"Unauthenticated user attempted to access AI post creation from IP: {request.META.get('REMOTE_ADDR')}")
        raise PermissionDenied("Musisz być zalogowany, aby uzyskać dostęp do tej strony.")

    if not request.user.is_staff:
        logger.warning(
            f"Non-staff user {request.user.username} attempted to access AI post creation from IP: {request.META.get('REMOTE_ADDR')}")
        raise PermissionDenied("Nie masz uprawnień do tworzenia postów AI. Skontaktuj się z administratorem.")

    if request.method == 'POST':
        form = AIPromptForm(request.POST)
        if form.is_valid():
            ai_prompt = None
            try:
                # Save the prompt with proper user attribution
                ai_prompt = form.save(commit=False)
                ai_prompt.created_by = request.user
                ai_prompt.save()

                logger.info(
                    f"Admin user {request.user.username} started AI generation with model: {ai_prompt.model_name}")

                # Call real AI API through service layer
                ai_response = generate_ai_blog_post(
                    model_name=ai_prompt.model_name,
                    prompt=ai_prompt.prompt_text
                )

                # Create the blog post with AI-generated content
                post = Post.objects.create(
                    title=ai_response.title,
                    content=ai_response.content,
                    author=ai_prompt.model_name,
                    latitude=ai_response.latitude,
                    longitude=ai_response.longitude,
                    ai_prompt=ai_prompt
                )

                logger.info(
                    f"Successfully created post: {post.title} (ID: {post.pk}) by admin {request.user.username}")

                messages.success(
                    request,
                    f'✅ Sukces! Post "{post.title}" został wygenerowany przez {ai_prompt.model_name} i opublikowany.'
                )
                return redirect('blog:post_detail', pk=post.pk)

            except ValueError as e:
                # Configuration/validation errors
                logger.error(f"Configuration error for user {request.user.username}: {str(e)}")
                if ai_prompt:
                    ai_prompt.delete()  # Clean up if post creation failed
                messages.error(
                    request,
                    f'❌ Błąd konfiguracji: {str(e)}'
                )
            except Exception as e:
                # API or other errors
                logger.error(f"AI generation error for user {request.user.username}: {str(e)}", exc_info=True)
                if ai_prompt:
                    ai_prompt.delete()  # Clean up if post creation failed
                messages.error(
                    request,
                    f'❌ Błąd podczas generowania posta: {str(e)}'
                )
        else:
            messages.error(
                request,
                '❌ Formularz zawiera błędy. Proszę sprawdzić wprowadzone dane.'
            )
    else:
        form = AIPromptForm()

    # Get recent AI-generated posts for display (only for staff users)
    recent_ai_posts = Post.objects.filter(ai_prompt__isnull=False).order_by('-created_at')[:5]

    context = {
        'form': form,
        'recent_ai_posts': recent_ai_posts,
        'user_can_create_ai_posts': True,  # Already verified above
    }
    return render(request, 'blog/add_ai_post.html', context)


@staff_member_required
def ai_post_status(request):
    """
    API endpoint to check if user has permission to create AI posts
    Returns JSON response indicating access level
    """
    return JsonResponse({
        'has_access': True,
        'user': request.user.username,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'permissions': list(request.user.user_permissions.values_list('codename', flat=True))
    })

