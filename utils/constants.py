from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class STAGES(models.TextChoices):
    INITIATION = 'initiation', 'Initiation'
    DEVELOPMENT = 'development', 'Development'
    TESTING = 'testing', 'Testing'
    DEPLOYMENT = 'deployment', 'Deployment'
    GOLIVE = 'golive', 'Go-Live'
    POSTGOLIVE = 'pgolive', 'Post Go-Live'


class STATUS(models.TextChoices):
    ACTIVE = 'active', 'Active'
    ONHOLD = 'onhold', 'On Hold'
    CLOSED = 'closed', 'Closed'


class DocumentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUBMITTED = 'submitted', 'Submitted'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    WAIVED = 'waived', 'Waived'


class ApprovalDecision(models.TextChoices):
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    WAIVED = 'waived', 'Waived'


class Actions(models.TextChoices):
    CREATED = 'created', 'Created'
    SUBMITTED = 'submitted', 'Submitted'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    WAIVED = 'waived', 'Waived'
    STAGEADVANCED = 'stage-advanced', 'Stage Advanced'
    REASSIGNED = 'reassigned', 'Reassigned'
    HANDOVER = 'handover', 'Handover'


class Roles(models.TextChoices):
    PM = "pm", "Project Manager"
    PMO_HEAD = "pmo_head", "Head, Project Management"


PENDING_DOC_PARAM = [
    OpenApiParameter(
        name="initiative_id",
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description="Initiative ID",
        required=True,
    ),
]

BLOCKING_DOC_PARAM = [
    OpenApiParameter(
        name="initiative_id",
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description="Initiative ID",
        required=True,
    ),
    OpenApiParameter(
        name="stage",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Initiative Stage",
        required=True,
    ),
]

DOC_NAME_PARAM = [
    OpenApiParameter(
        name="document_name",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Document Name",
        required=True,
    )
]
