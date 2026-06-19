from django.db.models import QuerySet
from django.utils import timezone
from api.auth.models import User
from api.core.models import InitiativeDocument, InitiativeType, StageRequirementTemplate, Initiative
from api.core.repositories.initiative import InitiativeTypeRepository, StageRequirementTemplateRepository, \
    InitiativeDocumentRepository, InitiativeRepository
from api.core.services.governance import AuditLogService
from utils.constants import DocumentStatus, Actions


class InitiativeTypeService:
    def __init__(self):
        self.repo = InitiativeTypeRepository()

    def create_type(self, name):
        data = {
            'name': name
        }
        return self.repo.create(**data)

    def get_type_by_id(self, type_id):
        return self.repo.get_by_id(id=type_id)

    def get_all_types(self):
        return self.repo.get_all()


class InitiativeService:
    def __init__(self):
        self.repo = InitiativeRepository()

    def get_by_initiative_id(self, initiative_id):
        initiative = self.repo.get_by_id(id=initiative_id)
        return initiative


class StageRequirementTemplateService:
    def __init__(self):
        self.repo = StageRequirementTemplateRepository()

    def create_template(self, initiative_type_id, stage: str, document_name: str,
                        is_required: bool = True):
        initiative_type = InitiativeTypeService().get_type_by_id(initiative_type_id)

        template_data = {
            'initiative_type': initiative_type,
            'stage': stage,
            'is_required': is_required,
            'document_name': document_name
        }
        return self.repo.create(**template_data)

    def get_template(self, initiative_type_id = None, stage: str = None):
        initiative_type = InitiativeTypeService().get_type_by_id(initiative_type_id)

        if initiative_type and stage:
            return self.repo.get_by_initiative_type_and_stage(initiative_type=initiative_type, stage=stage)

        if initiative_type:
            return self.repo.get_by_initiative_type(initiative_type=initiative_type)

        return self.repo.get_all()

    def update_template(self, template_id, data_update: dict):
        requirement_template = self.repo.get_by_id(id=template_id)
        if not requirement_template:
            return None
        return self.repo.update(requirement_template, **data_update)

    def delete_template(self, template_id):
        requirement_template = self.repo.get_by_id(id=template_id)
        self.repo.delete(requirement_template)


class InitiativeDocumentService:
    def __init__(self):
        self.repo = InitiativeDocumentRepository()

    def generate_checklist_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_initiative_id(initiative_id)
        return self.repo.generate_checklist(initiative)

    def submit_document(self, initiative_id, document_name, user):
        initiative: Initiative = InitiativeService().get_by_initiative_id(initiative_id)
        document_to_submit = self.repo.get_submission_template(initiative, document_name)
        data_to_update = {
            'submitted_by': user,
            'submitted_at': timezone.now(),
            'status': DocumentStatus.SUBMITTED
        }
        submission = self.repo.update(document_to_submit, **data_to_update)
        AuditLogService().log(initiative, Actions.SUBMITTED, user, submission)
        return submission

    def waive_document(self, initiative_id, document_name, waiver_reason, user):
        initiative: Initiative = InitiativeService().get_by_initiative_id(initiative_id)
        document_to_waive = self.repo.get_submission_template(initiative, document_name)
        data_to_update = {
            'status': DocumentStatus.WAIVED,
            'waiver_reason': waiver_reason
        }
        waiver = self.repo.update(document_to_waive, **data_to_update)
        AuditLogService().log(initiative, Actions.WAIVED, user, waiver)
        return waiver

    def get_documents(self):
        return self.repo.get_all()

    def get_documents_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_initiative_id(initiative_id)
        return self.repo.get_by_initiative(initiative)

    def get_pending_approvals_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_initiative_id(initiative_id)
        return self.repo.get_pending_approvals(initiative)