from django.urls import reverse
from django.shortcuts import redirect

class LoginRequireMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_routes = [
            '/myblog_app/delete/',
            '/index/',
        ]
        login_url = reverse('log-in')

        if request.path.startswith('/static/') or request.path == login_url:
            return self.get_response(request)

        if any(request.path.startswith(p) for p in protected_routes):
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect(login_url)

        return self.get_response(request)
