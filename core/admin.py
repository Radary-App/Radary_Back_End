from .models import User,Review, Problem, Emergency, AI_Emergency, AI_Problem, Authority, Authority_Locations
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class UserAdminCustom(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz')
    search_fields = ('email', 'username', 'first_name',"last_name",  'phone_number', 'governorate', 'markaz') 
    list_filter = ('is_admin', "governorate", "markaz")
    fieldsets = list(UserAdmin.fieldsets)   
    fieldsets[1][1]["fields"] = [
        "first_name",
        "last_name",
        "phone_number",
      
        "email",
        "image",
        "governorate",
        "markaz",
    ]

# ---------------------------
# Customizing Report admin view

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('status',"user", 'user_description',  'coordinates', "conclusion")
    search_fields = ('user', "user_description", "conclusion", "coordinates")
    list_filter = ('status', "user")

    inlines = [
        ReviewInline
    ]
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'coordinates', "created_at")
    search_fields = ('user', "coordinates")
    list_filter = ('user', )

# ---------------------------
# Customizing AI admin view
class AI_ProblemAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'priority', 'authority_name')
    search_fields = ('description', 'priority', "title")
    list_filter = ('priority', 'authority_name')

class AI_EmergencyAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'danger_level', 'authority_name')
    search_fields = ('description', 'danger_level')
    list_filter = ('danger_level', 'authority_name')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('related_user',  'comment',"difficulty","is_solved",  'created_at')
    search_fields = ('related_user', 'related_report', 'comment')
    list_filter = (
        "is_solved" ,"difficulty", 

    )


# Registering models in Django admin
admin.site.register(User, UserAdminCustom)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(AI_Problem, AI_ProblemAdmin)

admin.site.register(Authority)
admin.site.register(Authority_Locations)

admin.site.register(Emergency, EmergencyAdmin)
admin.site.register(AI_Emergency, AI_EmergencyAdmin)


admin.site.register(Review, ReviewAdmin)

