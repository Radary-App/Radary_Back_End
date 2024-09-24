# from .models import User,Review, Problem, Emergency, AI_Emergency, AI_Problem, Authority, Authority_Locations
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# class UserAdminCustom(UserAdmin):
#     list_display = ('email', 'username', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz')
#     search_fields = ('email', 'username', 'first_name',"last_name",  'phone_number', 'governorate', 'markaz') 
#     list_filter = ('is_admin', "governorate", "markaz")
#     fieldsets = list(UserAdmin.fieldsets)   
#     fieldsets[1][1]["fields"] = [
#         "first_name",
#         "last_name",
#         "phone_number",
      
#         "email",
#         "image",
#         "governorate",
#         "markaz",
#     ]

# # ---------------------------
# # Customizing Report admin view

# class ReviewInline(admin.TabularInline):
#     model = Review
#     extra = 0

# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ('status',"user", 'user_description',  'coordinates', "conclusion")
#     search_fields = ('user', "user_description", "conclusion", "coordinates")
#     list_filter = ('status', "user")

#     inlines = [
#         ReviewInline
#     ]
# class EmergencyAdmin(admin.ModelAdmin):
#     list_display = ('user', 'coordinates', "created_at")
#     search_fields = ('user', "coordinates")
#     list_filter = ('user', )

# # ---------------------------
# # Customizing AI admin view
# class AI_ProblemAdmin(admin.ModelAdmin):
#     list_display = ('report', 'title', 'description', 'priority', 'authority_name')
#     search_fields = ('description', 'priority', "title")
#     list_filter = ('priority', 'authority_name')

# class AI_EmergencyAdmin(admin.ModelAdmin):
#     list_display = ('report', 'title', 'description', 'danger_level', 'authority_name')
#     search_fields = ('description', 'danger_level')
#     list_filter = ('danger_level', 'authority_name')

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('related_user',  'comment',"difficulty","is_solved",  'created_at')
#     search_fields = ('related_user', 'related_report', 'comment')
#     list_filter = (
#         "is_solved" ,"difficulty", 

#     )


# # Registering models in Django admin
# admin.site.register(User, UserAdminCustom)

# admin.site.register(Problem, ProblemAdmin)
# admin.site.register(AI_Problem, AI_ProblemAdmin)

# admin.site.register(Authority)
# admin.site.register(Authority_Locations)

# admin.site.register(Emergency, EmergencyAdmin)
# admin.site.register(AI_Emergency, AI_EmergencyAdmin)


# admin.site.register(Review, ReviewAdmin)

from .models import (
    User, Review, Problem, Emergency, AI_Emergency, AI_Problem, Authority, Authority_Locations, 
    Problem_Authority_Location, Emergency_Authority_Location
)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Customizing User admin view
class UserAdminCustom(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'date_of_birth', 'phone_number', 'governorate', 'markaz')
    search_fields = ('email', 'username', 'first_name', "last_name", 'phone_number', 'governorate', 'markaz')
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


# Inline view for displaying Reviews related to a Problem
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


# Inline view for linking Problems to Authority Locations
class ProblemAuthorityLocationInline(admin.TabularInline):
    model = Problem_Authority_Location
    extra = 0


# Inline view for linking Emergencies to Authority Locations
class EmergencyAuthorityLocationInline(admin.TabularInline):
    model = Emergency_Authority_Location
    extra = 0


class AuthorityNameFilter(admin.SimpleListFilter):
    title = 'Authority Name'
    parameter_name = 'authority_name'

    def lookups(self, request, model_admin):
        authorities = set([
            (p.ai.authority_name, p.ai.authority_name) 
            for p in Problem.objects.filter(id__in=[19, 20])
            if p.ai is not None
        ])
        return sorted(authorities)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ai__authority_name=self.value())
        return queryset

# Customizing Problem admin view
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('status', 'user', 'user_description', 'coordinates', 'conclusion', 'authority_name')
    search_fields = ('user', 'user_description', 'conclusion', 'coordinates')
    list_filter = ('status', 'user', AuthorityNameFilter)

    inlines = [
        ReviewInline,
        ProblemAuthorityLocationInline,
    ]


    def authority_name(self, obj):
        return obj.ai.authority_name if obj.ai else None

    authority_name.short_description = 'Authority Name'



# Customizing Emergency admin view
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'coordinates', "created_at")
    search_fields = ('user', "coordinates")
    list_filter = ('user', )

    inlines = [
        EmergencyAuthorityLocationInline,
    ]


# Customizing Authority admin view with location-based filtering
class AuthorityLocationInline(admin.TabularInline):
    model = Authority_Locations
    extra = 0


class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')
    inlines = [AuthorityLocationInline]


# Customizing AI Problem admin view
class AI_ProblemAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'priority', 'authority_name')
    search_fields = ('description', 'priority', "title")
    list_filter = ('priority', 'authority_name')


# Customizing AI Emergency admin view
class AI_EmergencyAdmin(admin.ModelAdmin):
    list_display = ('report', 'title', 'description', 'danger_level', 'authority_name')
    search_fields = ('description', 'danger_level')
    list_filter = ('danger_level', 'authority_name')


# Customizing Review admin view
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('related_user', 'comment', "difficulty", "is_solved", 'created_at')
    search_fields = ('related_user', 'related_report', 'comment')
    list_filter = ("is_solved", "difficulty")


# Registering models in Django admin
admin.site.register(User, UserAdminCustom)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(AI_Problem, AI_ProblemAdmin)
admin.site.register(Authority, AuthorityAdmin)
admin.site.register(Authority_Locations)
admin.site.register(Emergency, EmergencyAdmin)
admin.site.register(AI_Emergency, AI_EmergencyAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Problem_Authority_Location)
admin.site.register(Emergency_Authority_Location)
