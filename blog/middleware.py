from django.core.exceptions import PermissionDenied
from django.shortcuts import render


class NgrokSkipWarningMiddleware:
    """Middleware to add header that skips ngrok browser warning"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add header to skip ngrok warning page
        response['ngrok-skip-browser-warning'] = '1'
        return response


class PermissionDeniedMiddleware:
    """Middleware to handle PermissionDenied exceptions with custom 403 page"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return render(request, 'blog/403.html', status=403)


