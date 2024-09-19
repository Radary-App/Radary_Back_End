from .models import User, Problem, Emergency, AI_Emergency, AI_Problem, Authority, Authority_Locations
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz')
    search_fields = ('email', 'username', 'first_name', 'phone_number')
    list_filter = ('is_admin',)


# -----------------------------
# Customizing Report admin view
class ProblmAdmin(admin.ModelAdmin):
    list_display = ('status', 'user', 'user_description',  'coordinates')
    search_fields = ('user',)
    list_filter = ('status',)


class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'coordinates')
    search_fields = ('user',)
    list_filter = ('coordinates',)

# ---------------------------
# Customizing AI admin view
class AI_ProblemAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'priority', 'authority_name')
    search_fields = ('description', 'priority')
    list_filter = ('priority', 'authority_name')

class AI_EmergencyAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'danger_level', 'authority_name')
    search_fields = ('description', 'danger_level')
    list_filter = ('danger_level', 'authority_name')

# Registering models in Django admin
admin.site.register(User, UserAdmin)

admin.site.register(Problem)
admin.site.register(AI_Problem, AI_ProblemAdmin)

admin.site.register(Authority)
admin.site.register(Authority_Locations)

admin.site.register(Emergency, EmergencyAdmin)
admin.site.register(AI_Emergency, AI_EmergencyAdmin)

