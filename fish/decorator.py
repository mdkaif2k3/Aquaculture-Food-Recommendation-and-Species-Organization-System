from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            admin_id = request.session.get('user_id')
            if admin_id == 999:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper