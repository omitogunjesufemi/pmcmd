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


stage_list = ['initiation', 'development', 'testing', 'deployment', 'golive', 'pgolive']


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
    STAGEADVANCED = 'stage_advanced', 'Stage Advanced'
    REASSIGNED = 'reassigned', 'Reassigned'
    HANDOVER = 'handover', 'Handover'
    UPDATED = 'updated', 'Updated'


class Roles(models.TextChoices):
    PM = "pm", "Project Manager"
    PMO_HEAD = "pmo_head", "Head, Project Management"


# ------------
# PARAMETERS
# ------------
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

Stage_Param = OpenApiParameter(
    name="stage",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Initiative Stage",
    required=False,
)

Status_Param = OpenApiParameter(
    name="status",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Initiative Status",
    required=False,
)

Page_Param = OpenApiParameter(
    name="page",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Pagination",
    required=False,
)

INITIATIVE_LIST_PARAMS = [
    OpenApiParameter(
        name="initiative_type_id",
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description="Initiative Type ID",
        required=False,
    ),
    OpenApiParameter(
        name="category_id",
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
        description="Category ID",
        required=False,
    ),
    Stage_Param,
    Status_Param,
    Page_Param
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
