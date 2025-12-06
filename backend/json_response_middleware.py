import json

from django.http import HttpResponse

class JSONResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si c'est une réponse API, forcer le content-type JSON
        if request.path.startswith("/api/"):
            if not response.has_header("Content-Type") or "text/html" in response.get(
                "Content-Type", ""
            ):
                response["Content-Type"] = "application/json"
            if not response.has_header('Content-Type') or 'text/html' in response.get('Content-Type', ''):
                response['Content-Type'] = 'application/json'

        return response
