from django.contrib import admin

from core.models import Poll


@admin.register(Poll)
class TopicAdmin(admin.ModelAdmin):

    list_display = ('question', 'created_at')

    @staticmethod
    def preview(obj):
        return obj.question[:40]
