from django.utils import timezone
from api.core.models import Initiative
from api.core.repositories.initiative import InitiativeTypeRepository, StageRequirementTemplateRepository, \
    InitiativeDocumentRepository, InitiativeRepository, CategoryRepository
from api.core.services.governance import AuditLogService, ApprovalService
from utils.constants import DocumentStatus, Actions, STAGES, STATUS
from rest_framework.exceptions import NotFound
from utils.exceptions import InvalidStateTransitionException


class InitiativeTypeService:
    def __init__(self):
        self.repo = InitiativeTypeRepository()

    def create(self, name):
        data = {
            'name': name
        }
        return self.repo.create(**data)

    def get_by_id(self, type_id):
        initiative_type =  self.repo.get_by_id(id=type_id)
        if not initiative_type:
            raise NotFound(f"initiative Type with ID {type_id} was not found.")
        return initiative_type

    def get_all(self):
        return self.repo.get_all()

    def update(self, type_id, name):
        initiative_type = self.get_by_id(type_id)
        data = {
            'name': name
        }
        return self.repo.update(initiative_type, **data)


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def create(self, name):
        data = {
            'name': name
        }
        return self.repo.create(**data)

    def get_by_id(self, category_id):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise NotFound(f"Category with ID {category_id} was not found.")
        return category

    def get_all(self):
        return self.repo.get_all()

    def update(self, category_id, name):
        category = self.get_by_id(category_id)
        data = {
            'name': name
        }
        return self.repo.update(category, **data)


class InitiativeService:
    def __init__(self):
        self.repo = InitiativeRepository()

    def create(self, title, description, category_id, initiative_type_id, user):
        initiative_type = InitiativeTypeService().get_by_id(initiative_type_id)
        category = CategoryService().get_by_id(category_id)

        if not user:
            user = None
        data = {
            'title': title,
            'description': description,
            'category': category,
            'initiative_type': initiative_type,
            'current_stage': STAGES.INITIATION,
            'status': STATUS.ACTIVE,
            'owner': user,
        }
        initiative = self.repo.create(**data)
        InitiativeDocumentService().generate_checklist_for_initiative(initiative.id)
        return initiative

    def get_by_id(self, initiative_id):
        initiative = self.repo.get_by_id(id=initiative_id)
        if not initiative:
            raise NotFound(f"Initiative with ID {initiative_id} was not found.")
        return initiative

    def get_all(self):
        return self.repo.get_all()

    def update(self, initiative_id, **data_update):
        initiative = InitiativeService().get_by_id(initiative_id)
        InitiativeTypeService().get_by_id(data_update.get('initiative_type_id'))
        CategoryService().get_by_id(data_update.get('category_id'))
        return self.repo.update(initiative, **data_update)


class StageRequirementTemplateService:
    def __init__(self):
        self.repo = StageRequirementTemplateRepository()

    def create(self, initiative_type_id, stage: str, document_name: str,
                        is_required: bool = True):
        initiative_type = InitiativeTypeService().get_by_id(initiative_type_id)
        template_data = {
            'initiative_type': initiative_type,
            'stage': stage,
            'is_required': is_required,
            'document_name': document_name
        }
        return self.repo.create(**template_data)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, template_id):
        requirement_template = self.repo.get_by_id(id=template_id)
        if not requirement_template:
            raise NotFound(f"Stage Requirement Template with ID {template_id} was not found.")
        return requirement_template

    def get_by_initiative_type(self, initiative_type_id, stage: str = None):
        initiative_type = InitiativeTypeService().get_by_id(initiative_type_id)

        if stage:
            return self.repo.get_by_initiative_type_and_stage(initiative_type=initiative_type, stage=stage)

        return self.repo.get_by_initiative_type(initiative_type=initiative_type)

    def update(self, template_id, **data_update):
        requirement_template = self.repo.get_by_id(id=template_id)
        if not requirement_template:
            raise NotFound(f"Stage Requirement Template with ID {template_id} was not found.")

        initiative_type_id = data_update.pop('initiative_type_id', None)
        if initiative_type_id:
            data_update['initiative_type'] = InitiativeTypeService().get_by_id(initiative_type_id)

        return self.repo.update(requirement_template, **data_update)

    def delete_template(self, template_id):
        requirement_template = self.repo.get_by_id(id=template_id)
        if not requirement_template:
            raise NotFound(f"Stage Requirement Template with ID {template_id} was not found.")

        self.repo.delete(requirement_template)


class InitiativeDocumentService:
    def __init__(self):
        self.repo = InitiativeDocumentRepository()

    def generate_checklist_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        existing_documents = self.repo.get_by_initiative(initiative)

        if existing_documents.exists():
            raise InvalidStateTransitionException("Checklist has already been generated for this initiative.")

        return self.repo.generate_checklist(initiative)

    def submit_document(self, initiative_id, document_name, user):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        document_to_submit = self.repo.get_submission_template(initiative, document_name)
        if not document_to_submit:
            raise NotFound(f"The document for this initiative {initiative_id}  was not found.")

        if document_to_submit.status in [DocumentStatus.SUBMITTED,
                                         DocumentStatus.WAIVED, DocumentStatus.APPROVED]:
            raise InvalidStateTransitionException("Only pending or rejected documents can be submitted.")

        data_to_update = {
            'submitted_by': user,
            'submitted_at': timezone.now(),
            'status': DocumentStatus.SUBMITTED
        }
        submission = self.repo.update(document_to_submit, **data_to_update)
        AuditLogService().log(initiative, Actions.SUBMITTED, user, submission)
        return submission

    def waive_document(self, initiative_id, document_id, waiver_reason, user):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        waiver = ApprovalService().waive_document(document_id, user, waiver_reason)
        AuditLogService().log(initiative, Actions.WAIVED, user, waiver)
        return waiver

    def get_documents(self):
        return self.repo.get_all()

    def get_documents_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        return self.repo.get_by_initiative(initiative)

    def get_pending_approvals_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        return self.repo.get_pending_approvals(initiative)
