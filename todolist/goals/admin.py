from django.contrib import admin
from todolist.goals.models import GoalCategory, Goal

@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    list_filter = ('is_deleted',)

# admin.site.register(GoalCategory, GoalCategoryAdmin)
# admin.site.register(Goal)

