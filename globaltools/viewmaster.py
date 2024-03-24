from django.core.handlers.wsgi import WSGIRequest
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, redirect


class ViewMaster:
    """
    A class responsible for making sure I write less redundant code
    """
    render_dest: str
    page_title: str

    # 'private' fields
    _context: dict
    _requires_login = False
    _redirect_dest: str

    def __init__(self, page_title: str, render_dest: str):
        self.page_title = page_title
        self.render_dest = render_dest

        # By default, the only thing in the context dictionary is the page_title
        self._context = {
            "page_title": page_title
        }

    def view(self, request):
        if self._requires_login and request.session.get('user_id', -1) < 0:
            return redirect(self._redirect_dest)
        return render(request, self.render_dest, self._context)

    def update_context(self, update_with):
        self._context.update(update_with)

    def require_login(self, redirect = None):
        if not redirect:
            self._requires_login = False
        else:
            self._requires_login = True

        self._redirect_dest = redirect



class FormView(ViewMaster):
    form: Form
    post_render_dest: str
    
    def __init__(self, page_title: str, render_dest: str, form):
        super().__init__(page_title, render_dest)
        self.post_render_dest = self.render_dest
        self.form = form
    
    def view(self, request: WSGIRequest):
        if request.method == "GET":
            return self.view_get(request)
        elif request.method == "POST":
            return self.view_post(request)

    def view_get(self, request: WSGIRequest):
        self.update_context({"form": self.form})
        return super().view(request)

    def view_post(self, request: WSGIRequest):
        post_form = Form(request.POST)
        if post_form.is_valid():
            return render(request, self.post_render_dest, self._context)
        else:
            self.update_context({""})
        
    
    