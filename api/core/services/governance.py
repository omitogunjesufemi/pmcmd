from api.core.repositories.governance import AuditLogRepository
from api.core.models import Initiative, InitiativeDocument, Approval
from api.auth.models import User


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
        self.repo = Approval

    def accept_document(self, comment=None):
        pass

    def reject_document(self, comment=None):
        pass

    def waive_document(self, comment=None):
        pass