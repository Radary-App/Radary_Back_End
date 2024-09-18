from .models import User, Report, AI
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_admin')
    search_fields = ('email', 'username')
    list_filter = ('is_admin',)


# -----------------------------
# Customizing Report admin view
class ReportAdmin(admin.ModelAdmin):
    list_display = ('category', 'status', 'user', 'coordinates')
    search_fields = ('user',)
    list_filter = ('category', 'status')


# ---------------------------
# Customizing AI admin view
class AIAdmin(admin.ModelAdmin):
    list_display = ('report', 'description', 'solution', 'danger_level')
    search_fields = ('description', 'solution')
    list_filter = ('danger_level',)



# Registering models in Django admin
admin.site.register(User, UserAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(AI, AIAdmin)

