from django.contrib import admin
from .models import User, Rule

admin.site.register(Rule)
admin.site.register(User)
