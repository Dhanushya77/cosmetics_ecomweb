from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(product)
admin.site.register(Category)
admin.site.register(Details)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Buy)