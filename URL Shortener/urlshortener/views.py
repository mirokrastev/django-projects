from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from urlshortener.common import generate_alias
from urlshortener.models import URLModel
from urlshortener.forms import URLForm
from django.http import Http404


class HomeView(FormView):
    form_class = URLForm
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.method not in ('GET', 'POST'):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        alias = form.cleaned_data['alias']
        url = form.cleaned_data['url']

        form = form.save(commit=False)
        form.alias = alias or generate_alias(url)
        form.save()

        context = super().get_context_data()
        context['alias'] = form.alias

        return render(self.request, 'urlshortener/success.html', context)


class RedirectToURL(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.method not in ('GET', 'POST'):
            raise Http404
        self.alias = self.kwargs['alias']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.redirect()

    def post(self, request, *args, **kwargs):
        return self.redirect()

    def redirect(self):
        try:
            url = URLModel.objects.get(alias=self.alias).url
            return redirect(url)
        except URLModel.DoesNotExist:
            return render(self.request, 'urlshortener/fail.html')
