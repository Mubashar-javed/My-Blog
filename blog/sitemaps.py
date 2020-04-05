from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSiteMap(Sitemap):
    # these both can be either method or attributes.
    changefreq = 'weekly'
    priority = 0.9  # max value is 1

    def items(self):
        """ this will return QuerySet to add items into our sitemaps"""
        return Post.published.all()

    def lastmod(self, obj):
        # we will get obj from our items() method  
        
        return obj.updated

    
