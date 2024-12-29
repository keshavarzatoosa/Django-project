from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Article, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView


class ArticleList(ListView):
    # model = Article
    # template_name = "blog/home.html"
    # context_object_name = "articles"
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


class CategoryList(ListView):
    paginate_by = 3
    template_name = "blog/category_list.html"
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


# def home(request, page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 3)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         # 'articles': Article.objects.all()
#         # 'articles': Article.objects.filter(status="p").order_by('-publish')[:3]
#         'articles': articles,
#         }
#     return render(request, "blog/home.html", context)

# def detail(request, slug):
#     # try:
#     #     article = Article.objects.get(slug=slug)
#     # except Exception as e:
#     #     raise Http404
#     # context = {
#     #     'article': article
#     #     }
#     context = {
#         'article': get_object_or_404(Article.objects.published(), slug=slug)
#         }
#     return render(request, "blog/detail.html", context)

# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 3)
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles
#         }
#     return render(request, "blog/category.html", context)

# def detail(request, slug):
#     context = {
#         'article': Article.objects.get(slug=slug)
#         }
#     return render(request, "blog/detail.html", context)

# def api(request):
#     return JsonResponse({"name": "eli", "family": "ahmadi"})
