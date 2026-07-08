from sys import int_info
from typing import List
from django.db.models import QuerySet
from api.auth.models import User
from api.core.models import Initiative, InitiativeType, Category, StageRequirementTemplate
from api.core.repositories.base import BaseRepository
from api.core.models import InitiativeDocument
from utils.constants import DocumentStatus


class InitiativeRepository(BaseRepository):
    model = Initiative

    def get_all_with_filters(self, stage=None, status=None,
                             category=None, initiative_type=None, owner=None) -> QuerySet[Initiative]:
        initiatives = (self.model.objects
                       .select_related('initiative_type', 'category', 'owner')
                       .all())
        if owner:
            initiatives = initiatives.filter(owner=owner)

        if stage:
            initiatives = initiatives.filter(current_stage=stage)

        if status:
            initiatives = initiatives.filter(status=status)

        if category:
            initiatives = initiatives.filter(category=category)

        if initiative_type:
            initiatives = initiatives.filter(initiative_type=initiative_type)

        return initiatives.order_by('-created_at')

    def get_by_id_with_relations(self, id):
        initiatives = (self.model.objects
                      .select_related('owner', 'category', 'initiative_type')
                      .prefetch_related('documents', 'audit_logs', 'handovers')
                      .filter(id=id)
                      .first())
        return initiatives


class InitiativeDocumentRepository(BaseRepository):
    model = InitiativeDocument

    def get_by_filters(self, initiative=None, submitted_by:User=None) -> QuerySet[InitiativeDocument]:
        documents = (self.model.objects
                     .select_related('initiative', 'submitted_by')
                     .all())
        if initiative:
            documents = documents.filter(initiative=initiative)

        if submitted_by:
            documents = documents.filter(submitted_by=submitted_by)
        return documents

    def get_submission_template(self, initiative, document_name) -> InitiativeDocument:
        document = (self.model.objects
                    .select_related('initiative', 'submitted_by')
                    .filter(initiative=initiative, document_name=document_name)
                    .first())
        return document

    def get_pending_approvals(self, initiative=None) -> QuerySet[InitiativeDocument]:
        documents = (self.model.objects
                     .select_related('initiative', 'submitted_by')
                     .filter(status=DocumentStatus.SUBMITTED))

        if initiative:
            documents = documents.filter(initiative=initiative)

        return documents

    def get_blocking_documents(self, initiative, stage:str) -> QuerySet[InitiativeDocument]:
        documents = (self.model.objects
                     .select_related('initiative', 'submitted_by')
                     .filter(initiative=initiative, stage=stage.lower(), is_required=True)
                     .exclude(status__in=[DocumentStatus.WAIVED, DocumentStatus.APPROVED]))
        return documents

    def generate_checklist(self, initiative) -> List[InitiativeDocument]:
        templates = StageRequirementTemplateRepository().get_by_initiative_type(initiative_type=initiative.initiative_type)
        documents = [
            InitiativeDocument(
                initiative=initiative,
                stage=template.stage,
                document_name=template.document_name,
                status=DocumentStatus.PENDING,
                is_required=template.is_required
            )
            for template in templates
        ]
        return self.model.objects.bulk_create(documents)


class StageRequirementTemplateRepository(BaseRepository):
    model = StageRequirementTemplate

    def get_by_initiative_type(self, initiative_type) -> QuerySet[StageRequirementTemplate]:
        requirement_templates = (self.model.objects
                 .select_related('initiative_type')
                 .filter(initiative_type=initiative_type))
        return requirement_templates

    def get_by_initiative_type_and_stage(self, initiative_type, stage) -> QuerySet[StageRequirementTemplate]:
        requirement_template = (self.model.objects
                                .select_related('initiative_type')
                                .filter(initiative_type=initiative_type, stage=stage))
        return requirement_template

    def delete(self, template):
        self.model.objects.filter(id=template.id).delete()


class InitiativeTypeRepository(BaseRepository):
    model = InitiativeType


class CategoryRepository(BaseRepository):
    model = Category