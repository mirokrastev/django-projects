from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import ContextMixin
from urlshortener.common import generate_alias
from urlshortener.models import URLModel
from urlshortener.forms import URLForm
from django.http import Http404


class HomeView(ContextMixin, View):
    form_class = URLForm
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'index.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = URLForm()
        return context


class CreateURL(ContextMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = URLForm(self.request.POST)
        if not form.is_valid():
            return self.form_invalid(form)
        return self.form_valid(form)

    def form_valid(self, form):
        alias = form.cleaned_data['alias']
        url = form.cleaned_data['url']

        form = form.save(commit=False)
        form.alias = alias or generate_alias(url)
        form.save()

        context = self.get_context_data()
        context['alias'] = form.alias

        return render(self.request, 'urlshortener/success.html', context)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, 'index.html', context)


class RedirectURL(View):
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
