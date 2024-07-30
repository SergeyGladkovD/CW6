from django.conf import settings
from django.core.cache import cache

from blog.models import Material


def get_cached_blogs():
    if settings.CACHE_ENABLED:
        key = "blog_list"
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Material.objects.all()
            cache.set(key, blog_list)
    else:
        blog_list = Material.objects.all()

    return blog_list
