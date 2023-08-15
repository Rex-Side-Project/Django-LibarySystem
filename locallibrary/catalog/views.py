from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.views import generic

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # The 'all()' is implied by default.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()  # __exact is the same as __iexact

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_visit = request.session.get('num_visit', 0)
    request.session['num_visit'] = num_visit + 1

    print(num_visit)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visit': num_visit,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    # your own name for the list as a template variable
    context_object_name = 'book_list'
    # Specify your own template name/location
    template_name = 'books/my_arbitrary_template_name_list.html'

    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        # Get 5 books containing the title war
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    # your own name for the list as a template variable
    context_object_name = 'author_list'
    # Specify your own template name/location
    template_name = 'authors/my_arbitrary_template_name_list.html'

    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        # Get 5 books containing the title war
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


class LoandBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
