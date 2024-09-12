from .models import User, Issue, AI
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_admin')
    search_fields = ('email', 'username')
    list_filter = ('is_admin',)


# -----------------------------
# Customizing Issue admin view
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'level', 'user')
    search_fields = ('title', 'address')
    list_filter = ('level',)


# ---------------------------
# Customizing AI admin view
class AIAdmin(admin.ModelAdmin):
    list_display = ('issue', 'ai_description', 'ai_solution', 'ai_danger_level')
    search_fields = ('ai_description', 'ai_solution')
    list_filter = ('ai_danger_level',)



# Registering models in Django admin
admin.site.register(User, UserAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(AI, AIAdmin)

