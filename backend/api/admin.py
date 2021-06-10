from django.contrib import admin

from api.models import Poll, Choice, Result


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address')


@admin.register(Poll)
class TopicAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = ('question', 'created_at')

    @staticmethod
    def preview(obj):
        return obj.question[:40]


