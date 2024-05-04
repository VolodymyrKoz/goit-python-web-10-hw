from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.views import View
from django.views.generic.edit import CreateView
from .utils import get_mongodb
from .forms import AddQuoteForm, AuthorForm, QuoteForm
from .models import Tag
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import QuoteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
import json
from pathlib import Path
from django.http import HttpResponseBadRequest, Http404
from bson.objectid import ObjectId

def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:  # Specify encoding as 'utf-8'
        quotes_data = json.load(f)
    return quotes_data


def main(request, page=1):
    per_page = 10
    template_name = "quotes/index.html"
    db = get_mongodb()
    quotes = db.quoters.find()
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        template_name,
        context={"quotes": quotes_on_page, "paginator": paginator},
    )


class AuthorDetailView(View):
    template_name = "quotes/author.html"

    def get(self, request, name: str):
        db = get_mongodb()
        author = db.authors.find_one({"name": name})
        if not author:
            raise Http404("Author not found")
        return render(request, self.template_name, context={"author": author})


class AddAuthorView(CreateView):
    template_name = "quotes/add_author.html"
    form_class = AuthorForm
    success_url = reverse_lazy("quotes:root")

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return HttpResponseBadRequest("Invalid form submission. Please check the form data.")


class TagDetailView(View):
    template_name = "quotes/quote_list.html"

    def get(self, request, name: str):
        db = get_mongodb()
        quotes = list(db.quoters.find({"tags": name}))
        context = {"tag": name, "quotes": quotes}
        return render(request, self.template_name, context)


class AddQuoteView(LoginRequiredMixin, CreateView):
    template_name = "quotes/add_quote.html"
    form_class = QuoteForm
    success_url = reverse_lazy("quotes:root")

    def form_valid(self, form):
        quote = form.save(commit=False)
        quote.user = self.request.user
        quote.save()
        return super().form_valid(form)
