from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render


class ViewMaster:
    render_dest: str
    page_title: str
    _context: dict

    def __init__(self, page_title: str, render_dest: str):
        self.page_title = page_title
        self.render_dest = render_dest

        # By default, the only thing in the context dictionary is the page_title
        self._context = {
            "page_title": page_title
        }

    def view(self, request):
        return render(request, self.render_dest, self._context)

    def update_context(self, update_with):
        self._context.update(update_with)


class FormView(ViewMaster):
    form: Form
    
    def __init__(self, page_title: str, render_dest: str, form):
        super().__init__(page_title, render_dest)
        self.update_context({"form": form})
    
    def view(self, request):
        if request.method == "GET":
            return self.view_get(request)
        elif request.method == "POST":
            return self.view_post(request)

    def view_get(self, request):
        self.update_context({"form": self.form})
        return super().view(request)

    def view_post(self, request):
        pass
        
    
    