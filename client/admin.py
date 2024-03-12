from django.contrib import admin

from client.models import Quote, Customer, TypeformResponse, DailyFormResponse


class TypeformChoiceInline(admin.StackedInline):
    model = TypeformResponse
    extra = 1


class DailyFormChoiceInline(admin.StackedInline):
    model = DailyFormResponse
    extra = 3


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["email"]
    list_filter = ["created_at"]
    list_display = ["email", "created_at"]
    # fieldsets = [
    #     (None, {"fields": ["question_text"]}),
    #     ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    # ]
    inlines = [TypeformChoiceInline, DailyFormChoiceInline]


# Register your models here.
admin.site.register(Quote)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(TypeformResponse)
admin.site.register(DailyFormResponse)
