from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .filters import SearchFilter
from .models import Quote, Category, Comment
from .forms import AddQuotesForm, CommentForm
from django.contrib.auth.decorators import login_required


class QuoteDetail(DetailView):
    model = Quote
    template_name = "quotes/quote_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Quote.objects.get(id=self.kwargs['pk'])
        context['total_likes'] = query.total_likes()
        context['post'] = Quote.objects.filter(author=query.author)
        context['post1'] = len(Quote.objects.filter(author=query.author))
        liked = False
        if query.users_like.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        return context


# def Home(request, id=None):
#     categories = Quote.objects.values("category").distinct()
#     search = SearchFilter(request.GET, queryset=Quote.objects.all().order_by('-time'))
#     comment = Comment.objects.all()
#     if request.method == 'POST':
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             new_item = form.save(commit=False)
#             parent_id = request.Comment.objects.get(id='parent_id')
#             reply = None
#             if parent_id:
#                 reply = Comment.objects.get(id='parent_id')
#             form.parent = reply
#             new_item.author = request.user
#             new_item.save()
#             return redirect(new_item.get_absolute_url())
#
#     else:
#         form = CommentForm(data=request.GET)
#         return render(request, "quotes/all_quote.html",
#                       {'form': form, 'categories': categories, 'search': search, 'comment': comment})


class Home(CreateView):
    model = Quote
    form_class = CommentForm
    template_name = "quotes/all_quote.html"
    success_url = reverse_lazy('quotes:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Quote.objects.values("category").distinct()
        context['search'] = SearchFilter(self.request.GET, queryset=self.get_queryset().order_by('-time'))
        context['comment'] = Comment.objects.filter(parent=None)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        parent_id = self.request.POST.get('parent_id')
        reply = None
        if parent_id:
            reply = Comment.objects.get(id=parent_id)
        form.instance.parent = reply
        return super(Home, self).form_valid(form)


@login_required()
def add_quotes(request):
    if request.method == 'POST':
        form = AddQuotesForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.author = request.user
            new_item.save()
            return redirect(new_item.get_absolute_url())

    else:
        form = AddQuotesForm(data=request.GET)
        return render(request, "quotes/add_quotes.html", {'form': form})


#
# class AddQuote(CreateView):
#     model = Quote
#     form_class = AddQuotesForm
#     template_name = "quotes/add_quotes.html"
#     success_url = reverse_lazy(Quote.get_absolute_url)
#
#     def get_object(self, queryset=None):
#         return self.request.user


class QuoteDelete(DeleteView):
    model = Quote
    template_name = "quotes/quote_delete.html"
    success_url = reverse_lazy('quotes:home')


class QuoteUpdate(UpdateView):
    model = Quote
    form_class = AddQuotesForm
    template_name = "quotes/quote_update.html"


class AddCategory(CreateView):
    model = Category
    template_name = "quotes/add_category.html"
    fields = '__all__'
    success_url = reverse_lazy('quotes:add_quotes')


def Categories(request, category):
    categories = Quote.objects.filter(category=category.replace('-', ' ').title())
    if not categories:
        categories = Quote.objects.filter(category=category.replace('-', ' '))
    elif not categories:
        categories = Quote.objects.filter(category=category.replace('-', ' ').capitalize())
    if not categories: categories = Quote.objects.filter(category=category.replace('-', ' ').upper())
    category_list = Quote.objects.values("category").distinct()
    return render(request, "quotes/categories.html",
                  {'category': category.replace('-', ' ').title(), 'categories': categories, 'category_list': category_list})


@login_required
def QuoteLike(request, pk):
    post = Quote.objects.get(id=pk)
    if post.users_like.filter(id=request.user.id).exists():
        post.users_like.remove(request.user)
    else:
        post.users_like.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def quoteLike(request):
    post = Quote.objects.get(id=request.POST.get('quote_pk'))
    if post.users_like.filter(id=request.user.id).exists():
        post.users_like.remove(request.user)
    else:
        post.users_like.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
