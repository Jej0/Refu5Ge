from django.shortcuts import redirect

from accounts.models import UserProfile


def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.profile.level != group_name:
                return redirect("all_rooms")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator