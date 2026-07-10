from django.db import transaction
from django.utils import timezone
from api.auth.models import User
from api.core.models import Initiative
from api.core.repositories.initiative import InitiativeTypeRepository, StageRequirementTemplateRepository, \
    InitiativeDocumentRepository, InitiativeRepository, CategoryRepository
from api.core.serializers import InitiativeDocumentOutputSerializer
from api.core.services.governance import AuditLogService, ApprovalService
from utils.constants import DocumentStatus, Actions, STAGES, STATUS, stage_list
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from utils.exceptions import InvalidStateTransitionException, ServiceException


class InitiativeTypeService:
    def __init__(self):
        self.repo = InitiativeTypeRepository()

    def create(self, name):
        data = {
            'name': name
        }
        return self.repo.create(**data)

    def get_by_id(self, type_id):
        initiative_type = self.repo.get_by_id(id=type_id)
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
        with transaction.atomic():
            initiative_type = InitiativeTypeService().get_by_id(initiative_type_id)
            category = CategoryService().get_by_id(category_id)

            if not user:
                raise InvalidStateTransitionException("This action requires a signed in user.")

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
            AuditLogService().log(initiative, Actions.CREATED, user)
            return initiative

    def get_by_id(self, initiative_id):
        initiative = self.repo.get_by_id(id=initiative_id)
        if not initiative:
            raise NotFound(f"Initiative with ID {initiative_id} was not found.")
        return initiative

    def get_by_id_and_owner(self, initiative_id, owner):
        initiative:Initiative = self.repo.get_by_id(id=initiative_id)
        if not initiative:
            raise NotFound(f"Initiative with ID {initiative_id} was not found.")

        if not owner:
            raise PermissionDenied("This user does not own this initiative.")

        if owner.id is not initiative.owner.id:
            raise PermissionDenied("This user doesn't have permission to update this initiative.")

        return initiative

    def get_all(self, stage=None, status=None, category_id=None, initiative_type_id=None, page=None, owner=None):
        category = None
        initiative_type = None
        if initiative_type_id:
            initiative_type = InitiativeTypeService().get_by_id(initiative_type_id)
        if category_id:
            category = CategoryService().get_by_id(category_id)
        initiatives = self.repo.get_all_with_filters(stage, status, category, initiative_type, owner)

        for initiative in initiatives:
            blocking_documents_count = len(InitiativeDocumentService().get_blocking_document_for_initiative(initiative.id, initiative.current_stage))
            initiative.blocking_documents_count = blocking_documents_count
        return initiatives

    def get_by_owner(self, owner: User):
        if not owner:
            raise NotFound("Owner not found.")
        initiatives = self.repo.get_all_with_filters(owner=owner)
        return initiatives

    def update(self, initiative_id, **data_update):
        with transaction.atomic():
            initiative = InitiativeService().get_by_id(initiative_id)
            owner = None

            if 'initiative_type_id' in data_update:
                InitiativeTypeService().get_by_id(data_update.get('initiative_type_id'))

            if 'category_id' in data_update:
                CategoryService().get_by_id(data_update.get('category_id'))

            if 'current_stage' in data_update:
                raise ServiceException("Cannot update 'current_stage' directly.")

            if 'owner' in data_update:
                owner = data_update.get('owner')
                if not owner:
                    raise PermissionDenied("This user doesn't have permission to update this initiative.")
                initiative = InitiativeService().get_by_id_and_owner(initiative_id, owner)

            updated_data = self.repo.update(initiative, **data_update)
            AuditLogService().log(initiative, Actions.UPDATED, owner)
            return updated_data

    def advance_stage(self, initiative_id, owner):
        initiative: Initiative = InitiativeService().get_by_id_and_owner(initiative_id, owner)
        prev_stage = initiative.current_stage
        blocking_documents = InitiativeDocumentService().get_blocking_document_for_initiative(initiative_id, prev_stage)
        blocking_documents_counts = len(blocking_documents)
        if blocking_documents_counts > 0:
            error_context = {
                'message': f"There are {blocking_documents_counts} required documents pending.",
                'error_code': 'STAGE_ADVANCEMENT_BLOCKED',
                'blocking_documents': InitiativeDocumentOutputSerializer(blocking_documents, many=True).data
            }
            raise ServiceException(error_context)

        if initiative.current_stage is STAGES.POSTGOLIVE:
            raise ServiceException("Initiative is already at final stage (PostGoLive)")

        if initiative.status is STATUS.CLOSED or initiative.status is STATUS.ONHOLD:
            raise ServiceException(f"Initiative Status is {initiative.status.capitalize()}")

        stage_idx = stage_list.index(prev_stage)
        if stage_idx >= len(stage_list) - 1:
            raise ServiceException("Initiative is already at final stage (PostGoLive)")

        new_stage = stage_list[stage_idx + 1]
        data_update = {
            'current_stage': new_stage
        }
        updated_initiative = self.repo.update(initiative, **data_update)

        return_data = {
            'id': updated_initiative.id,
            'previous_stage': prev_stage,
            'current_stage': updated_initiative.current_stage,
            'message': f"Initiative advanced to {updated_initiative.current_stage.capitalize()} stage."
        }
        AuditLogService().log(initiative, Actions.STAGEADVANCED, owner)
        return return_data


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
        existing_documents = self.repo.get_by_filters(initiative)

        if existing_documents.exists():
            raise InvalidStateTransitionException("Checklist has already been generated for this initiative.")

        return self.repo.generate_checklist(initiative)

    def submit_document(self, initiative_id, document_name, user):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        document_to_submit = self.repo.get_submission_template(initiative, document_name)
        if not document_to_submit:
            raise NotFound(f"The document ({document_name}) for this initiative {initiative_id}  was not found.")

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
        with transaction.atomic():
            initiative: Initiative = InitiativeService().get_by_id(initiative_id)
            waiver = ApprovalService().waive_document(document_id, user, waiver_reason)
            AuditLogService().log(initiative, Actions.WAIVED, user, waiver)
            return waiver

    def get_all(self):
        return self.repo.get_all()

    def get_documents_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        return self.repo.get_by_filters(initiative)

    def get_documents_for_owner(self, owner: User):
        return self.repo.get_by_filters(submitted_by=owner)

    def get_by_id(self, document_id):
        document = self.repo.get_by_id(document_id)
        if not document:
            raise NotFound(f"The document with {document_id} was not found.")
        return document

    def get_blocking_document_for_initiative(self, initiative_id, stage):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        return self.repo.get_blocking_documents(initiative, stage)

    def get_pending_approvals_for_initiative(self, initiative_id):
        initiative: Initiative = InitiativeService().get_by_id(initiative_id)
        return self.repo.get_pending_approvals(initiative)
