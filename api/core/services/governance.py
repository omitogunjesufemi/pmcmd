from django.db import transaction
from rest_framework.exceptions import NotFound

from api.auth.services import UserService
from api.core.repositories.governance import AuditLogRepository, ApprovalRepository, HandoverRepository
from api.core.repositories.initiative import InitiativeDocumentRepository
from api.core.models import Initiative, InitiativeDocument, Approval
from api.auth.models import User
from api.core.services.initiatives import InitiativeService
from utils.constants import DocumentStatus, ApprovalDecision, Actions, Roles
from utils.exceptions import ServiceException


class AuditLogService:
    def __init__(self):
        self.repo = AuditLogRepository()

    def log(self, initiative: Initiative, action: str, performed_by: User, document : InitiativeDocument =None, notes: str=None):
        audit_data = {
            'initiative': initiative,
            'action': action,
            'performed_by': performed_by,
            'document': document,
            'notes': notes
        }
        audit_log = self.repo.create(audit_action=audit_data)
        return audit_log

    def get_by_initiative(self, initiative_id):
        initiative = InitiativeService().get_by_id(initiative_id=initiative_id)
        return self.repo.get_by_initiative(initiative)


class ApprovalService:
    def __init__(self):
        self.repo = ApprovalRepository()

    def approve_document(self, document_id, user, comment=None):
        document_to_approve = InitiativeDocumentRepository().get_by_id(id=document_id)
        if not document_to_approve:
            raise NotFound(f"This document with ID {document_id} was not found.")

        data_to_update = {
            'status': DocumentStatus.APPROVED,
        }
        accepted = InitiativeDocumentRepository().update(document_to_approve, **data_to_update)
        self.repo.create(document=document_to_approve, reviewed_by=user,
                         decision=ApprovalDecision.APPROVED, comment=comment)
        return accepted

    def reject_document(self, document_id, user, comment=None):
        document_to_reject = InitiativeDocumentRepository().get_by_id(id=document_id)
        if not document_to_reject:
            raise NotFound(f"This document with ID {document_id} was not found.")

        data_to_update = {
            'status': DocumentStatus.REJECTED,
        }
        rejection = InitiativeDocumentRepository().update(document_to_reject, **data_to_update)
        self.repo.create(document=document_to_reject, reviewed_by=user,
                         decision=ApprovalDecision.REJECTED, comment=comment)
        return rejection

    def waive_document(self, document_id, user, comment=None):
        document_to_waive = InitiativeDocumentRepository().get_by_id(id=document_id)
        if not document_to_waive:
            raise NotFound(f"This document with ID {document_id} was not found.")

        data_to_update = {
            'status': DocumentStatus.WAIVED,
            'waiver_reason': comment,
        }
        waiver = InitiativeDocumentRepository().update(document_to_waive, **data_to_update)
        self.repo.create(document=document_to_waive, reviewed_by=user,
                         decision=ApprovalDecision.WAIVED, comment=comment)
        return waiver


class HandoverService:
    def __init__(self):
        self.repo = HandoverRepository()

    def create_handover(self, initiative_id, from_user, to_user_id, what_was_done, what_needs_doing):
        with transaction.atomic():
            from api.core.services.initiatives import InitiativeService
            print(f"Owner - {from_user}")
            initiative: Initiative = InitiativeService().get_by_id_and_owner(initiative_id, owner=from_user)
            to_user: User = UserService().get_by_id(to_user_id)
            if to_user.id == from_user.id:
                raise ServiceException(f"You cannot handover to yourself.")

            if to_user.role is not Roles.PM:
                raise ServiceException(f"The user you want to handover to is not a PM.")
            data = {
                'initiative': initiative,
                'from_user': from_user,
                'to_user':to_user,
                'what_was_done': what_was_done,
                'what_needs_doing': what_needs_doing
            }
            handover = self.repo.create(**data)
            h_stat = {
                'is_handed_over': True,
                'owner': from_user
            }
            InitiativeService().update(initiative_id, **h_stat)
            AuditLogService().log(initiative=initiative, action=Actions.HANDOVER, performed_by=from_user)
            return handover