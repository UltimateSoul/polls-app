from django.contrib import admin

from core.models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Poll)
class TopicAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = ('question', 'created_at')

    @staticmethod
    def preview(obj):
        return obj.question[:40]


