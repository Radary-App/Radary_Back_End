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
class AIAdmin(admin.ModelAdmin):
    list_display = ('report', 'description', 'solution', 'danger_level')
    search_fields = ('description', 'solution')
    list_filter = ('danger_level',)


# Registering models in Django admin
admin.site.register(User, UserAdmin)

admin.site.register(Problem)
admin.site.register(AI_Problem, AIAdmin)

admin.site.register(Authority)
admin.site.register(Authority_Locations)

admin.site.register(Emergency, EmergencyAdmin)
admin.site.register(AI_Emergency, AIAdmin)

