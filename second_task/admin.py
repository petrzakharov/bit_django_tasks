from django.contrib import admin

from second_task.models import LeadState, Lead

admin.site.register(LeadState)
admin.site.register(Lead)