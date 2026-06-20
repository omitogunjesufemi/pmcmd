from rest_framework.exceptions import NotFound

from api.core.repositories.governance import AuditLogRepository, ApprovalRepository
from api.core.repositories.initiative import InitiativeDocumentRepository
from api.core.models import Initiative, InitiativeDocument, Approval
from api.auth.models import User
from utils.constants import DocumentStatus, ApprovalDecision


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
