from django.db import models


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
