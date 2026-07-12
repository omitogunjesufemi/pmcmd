from api.core.serializers import InitiativeDocumentOutputSerializer, AuditLogOutputSerializer
from api.core.services.governance import AuditLogService
from api.core.services.initiatives import InitiativeService, InitiativeDocumentService
from utils.constants import STATUS, STAGES, DocumentStatus


class PMDashboardService:
    def pm_overview(self, owner):
        initiatives = InitiativeService().get_all(owner=owner)

        summary = {
            "total_initiatives": initiatives.count(),
            "active": initiatives.filter(status=STATUS.ACTIVE).count(),
            "on_hold": initiatives.filter(status=STATUS.ONHOLD).count(),
            "closed": initiatives.filter(status=STATUS.CLOSED).count()
        }

        by_stage = {
            "initiation": initiatives.filter(current_stage=STAGES.INITIATION).count(),
            "development": initiatives.filter(current_stage=STAGES.DEVELOPMENT).count(),
            "testing": initiatives.filter(current_stage=STAGES.TESTING).count(),
            "deployment": initiatives.filter(current_stage=STAGES.DEPLOYMENT).count(),
            "golive": initiatives.filter(current_stage=STAGES.GOLIVE).count(),
            "postgolive": initiatives.filter(current_stage=STAGES.POSTGOLIVE).count()
        }

        needs_attention = []
        recently_submitted = []
        recent_activities = []
        for initiative in initiatives:
            initiative_information = {
                "id": initiative.id,
                "title": initiative.title,
                "current_stage": initiative.current_stage,
                "blocking_documents_count": InitiativeDocumentService().get_blocking_document_for_initiative(
                    initiative_id=initiative.id, owner=owner).count()
            }
            recently_submitted.append(
                InitiativeDocumentOutputSerializer(
                    InitiativeDocumentService().get_documents_for_initiative(initiative_id=initiative.id, owner=owner, status=DocumentStatus.SUBMITTED),
                    many=True
                ).data
            )
            needs_attention.append(initiative_information)

            recent_activities.append(
                AuditLogOutputSerializer(
                    AuditLogService().get_by_initiative(initiative.id), many=True
                ).data
            )

        pm_overview_dashboard = {
            "summary": summary,
            "by_stage": by_stage,
            "needs_attention": needs_attention,
            "recently_submitted": recently_submitted,
            "recent_activity": recent_activities,
        }

        return pm_overview_dashboard