class NgrokSkipWarningMiddleware:
    """Middleware to add header that skips ngrok browser warning"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add header to skip ngrok warning page
        response['ngrok-skip-browser-warning'] = '1'
        return response

