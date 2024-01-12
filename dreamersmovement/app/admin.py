from django.contrib import admin
from .models import contact,joiners,donaters
# Register your models here.

admin.site.register(contact)
admin.site.register(joiners)
admin.site.register(donaters)