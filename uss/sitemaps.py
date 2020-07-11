from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from blogapp.models import Post

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(
            date_to_publish__lte=timezone.now()
        )

    def lastmod(self, obj):
        return obj.date_to_publish