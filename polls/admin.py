from django.contrib import admin

from polls.models import Question, Choice, Vote

# admin.site.site_header = 'Polls Administration'
# admin.site.site_title = 'Polls Administration'
# admin.site.index_title = 'Polls Administration'

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text', 'owner', 'pub_date', 'active', 'created_at', 'updated_at', 'was_published_recently']
    list_filter = ["active", 'created_at', 'pub_date']
    search_fields = ['question_text']
    date_hierarchy = 'pub_date'
    list_per_page = 10

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "poll", 'created_at', 'updated_at']
    search_fields = ["choice_text", "poll__text"]
    autocomplete_fields = ["poll"]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user", 'created_at']
    search_fields = ["choice__choice_text", "poll__text", "user__username"]
    autocomplete_fields = ["choice", "poll", "user"]
