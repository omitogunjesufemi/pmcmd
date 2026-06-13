from django.db import models
from api.auth.models import User
from utils.constants import STATUS, STAGES, DocumentStatus
from api.core.models.base import BaseModel


class InitiativeType(BaseModel):
    name = models.CharField(
        max_length=225,
        unique=True
    )

    class Meta:
        ordering = ['-created_at']


class Category(BaseModel):
    """Initiative Category"""
    name = models.CharField(max_length=225, unique=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Categories"

class Initiative(BaseModel):
    """Model for Initiatives"""
    title = models.CharField(max_length=225)
    description = models.TextField()
    current_stage = models.CharField(
        max_length=30,
        choices=STAGES.choices,
        default=STAGES.INITIATION
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS.choices,
        default=STATUS.ACTIVE
    )
    initiative_type = models.ForeignKey(
        InitiativeType,
        on_delete=models.PROTECT,
        related_name='initiatives'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='initiatives'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='initiatives'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class StageRequirementTemplate(BaseModel):
    initiative_type = models.ForeignKey(
        InitiativeType,
        on_delete=models.CASCADE,
        related_name='requirement_templates'
    )

    stage = models.CharField(
        max_length=30,
        choices=STAGES.choices,
    )

    is_required = models.BooleanField(default=True)

    document_name = models.CharField(
        max_length=225
    )

    def __str__(self):
        return f"{self.document_name} ({self.stage})"

    class Meta:
        ordering = ['stage']
        unique_together = [['initiative_type', 'stage', 'document_name']]


class InitiativeDocument(BaseModel):
    initiative = models.ForeignKey(
        Initiative,
        on_delete = models.CASCADE,
        related_name = 'submitted_documents'
    )
    stage = models.CharField(
        max_length=30,
        choices=STAGES.choices,
    )
    document_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30,
        choices=DocumentStatus.choices,
        default=DocumentStatus.PENDING
    )
    is_required = models.BooleanField(default=True)
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name = 'submitted_documents'
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    waiver_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_name} - {self.initiative.title} ({self.stage})"

    class Meta:
        ordering = ['stage', 'document_name']
        unique_together = [['initiative', 'stage', 'document_name']]
