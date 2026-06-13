from rest_framework import serializers
from api.auth.serializers import UserSerializer
from api.core.models.governance import Approval, AuditLog, Handover
from api.core.serializers.initiatives import (
    InitiativeDocumentOutputSerializer,
    InitiativeOutputSerializer,
)
from utils.constants import ApprovalDecision


class ApprovalInputSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    decision = serializers.ChoiceField(choices=ApprovalDecision.choices)
    comment = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False,
    )

    def validate(self, attrs):
        decision = attrs.get('decision')
        comment = attrs.get('comment')

        if isinstance(comment, str):
            comment = comment.strip()

        if decision in [ApprovalDecision.REJECTED, ApprovalDecision.WAIVED] and not comment:
            raise serializers.ValidationError({
                'comment': 'Comment is required when rejecting or waiving a document.'
            })

        attrs['comment'] = comment or ''
        return attrs


class ApprovalOutputSerializer(serializers.ModelSerializer):
    document = InitiativeDocumentOutputSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)

    class Meta:
        model = Approval
        fields = [
            'id', 'document', 'reviewed_by', 'decision',
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class AuditLogOutputSerializer(serializers.ModelSerializer):
    initiative = InitiativeOutputSerializer(read_only=True)
    document = InitiativeDocumentOutputSerializer(read_only=True)
    performed_by = UserSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'initiative', 'document', 'performed_by',
            'action', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class HandoverInputSerializer(serializers.Serializer):
    initiative_id = serializers.UUIDField()
    to_user_id = serializers.UUIDField()
    what_was_done = serializers.CharField()
    what_needs_doing = serializers.CharField()


class HandoverOutputSerializer(serializers.ModelSerializer):
    initiative = InitiativeOutputSerializer(read_only=True)
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Handover
        fields = [
            'id', 'initiative', 'from_user', 'to_user',
            'what_was_done', 'what_needs_doing', 'created_at', 'updated_at'
        ]
        read_only_fields = fields
