from typing import Type
from api.core.models import Approval, AuditLog, Handover, InitiativeDocument, Initiative
from api.auth.models import User
from api.core.repositories.base import BaseRepository
from django.db import models


class ApprovalRepository(BaseRepository):
    model = Approval

    def get_by_document(self, document: InitiativeDocument):
        approval = (self.model.objects
                    .select_related('document', 'reviewed_by')
                    .filter(document=document))
        return approval

    def get_by_initiative(self, initiative: Initiative):
        approvals = (self.model.objects
                     .select_related('document', 'reviewed_by')
                     .filter(document__initiative=initiative))
        return approvals


class AuditLogRepository:
    model : Type[models.Model] = AuditLog

    def get_by_initiative(self, initiative : Initiative):
        audit_logs = (self.model.objects
                      .select_related('initiative', 'document', 'performed_by')
                      .filter(initiative=initiative))
        return audit_logs

    def get_by_document(self, document: InitiativeDocument):
        audit_logs = (self.model.objects
                      .select_related('initiative', 'document', 'performed_by')
                      .filter(document=document))
        return audit_logs

    def create(self, audit_action: dict):
        audit_log = self.model.objects.create(**audit_action)
        return audit_log


class HandoverRepository(BaseRepository):
    model = Handover

    def get_by_initiative(self, initiative : Initiative):
        handover = (self.model.objects
                    .select_related('initiative', 'from_user', 'to_user')
                    .filter(initiative=initiative))
        return handover

    def get_by_user(self, user: User):
        handover = (self.model.objects
                    .select_related('initiative', 'from_user', 'to_user')
                    .filter(models.Q(from_user=user) |
                            models.Q(to_user=user)))
        return handover
