from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    
    def items(self):
        return Product.objects.filter(active=True).order_by("name")
    
    def lastmod(self, obj: Product):
        return obj.last_change_date