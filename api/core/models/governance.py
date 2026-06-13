from api.auth.models import User
from api.core.models.base import BaseModel
from django.db import models
from api.core.models.initiatives import InitiativeDocument, Initiative
from utils.constants import ApprovalDecision, Actions


class Approval(BaseModel):
    document = models.ForeignKey(
        InitiativeDocument,
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='approvals'
    )
    decision = models.CharField(
        max_length=30,
        choices=ApprovalDecision.choices,
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.document.document_name} - ({self.decision})"

    class Meta:
        ordering = ['created_at']


class AuditLog(BaseModel):
    initiative = models.ForeignKey(
        Initiative,
        on_delete=models.PROTECT,
        related_name='audit_logs'
    )
    document = models.ForeignKey(
        InitiativeDocument,
        on_delete=models.PROTECT,
        related_name='audit_logs',
        null=True,
        blank=True
    )
    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='audit_logs'
    )
    action = models.CharField(
        max_length=30,
        choices=Actions.choices,
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.action} - {self.performed_by.get_full_name()}'

    class Meta:
        ordering = ['-created_at']


class Handover(BaseModel):
    initiative = models.ForeignKey(
        Initiative,
        on_delete=models.PROTECT,
        related_name='handovers'
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='handovers_given'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='handovers_received'
    )
    what_was_done = models.TextField()
    what_needs_doing = models.TextField()

    def __str__(self):
        return f'{self.from_user.get_full_name()} - {self.to_user.get_full_name()}'

    class Meta:
        ordering = ['-created_at']