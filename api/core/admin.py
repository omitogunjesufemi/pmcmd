from django.contrib import admin
from api.core.models import (
    Category, InitiativeType, Initiative,
    StageRequirementTemplate, InitiativeDocument,
    Approval, AuditLog, Handover
)
from api.auth.models import User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(InitiativeType)
admin.site.register(Initiative)
admin.site.register(StageRequirementTemplate)
admin.site.register(InitiativeDocument)
admin.site.register(Approval)
admin.site.register(AuditLog)
admin.site.register(Handover)