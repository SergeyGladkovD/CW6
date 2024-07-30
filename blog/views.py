from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from blog.models import Material


class MaterialCreateView(CreateView):
    model = Material
    fields = ("title", "description", "image", "views_count")
    success_url = reverse_lazy("blog:list_blog")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class MaterialUpdateView(UpdateView):
    model = Material
    fields = ("title", "description", "image", "views_count")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:list_blog",
        )  # args=[self.kwargs.get("pk")]


class MaterialListView(ListView):
    model = Material

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = queryset.filter(published=True)
    #     return queryset


class MaterialDetailView(DetailView):
    model = Material

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     self.object.views += 1
    #     self.object.save()
    #     return self.object


class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy("blog:list_blog")
