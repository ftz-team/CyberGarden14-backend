from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Collector)
admin.site.register(Contact)
admin.site.register(Visit)
admin.site.register(VisitAchievement)
admin.site.register(Promotion)
admin.site.register(Achievement)