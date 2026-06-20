from rest_framework import serializers
from api.auth.serializers import UserSerializer
from api.core.models.initiatives import (InitiativeType, Category, InitiativeDocument,
                                         Initiative, StageRequirementTemplate)
from utils.constants import DocumentStatus, STAGES


class InitiativeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeType
        fields = [
            'id', 'name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InitiativeInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=225)
    description = serializers.CharField()
    category_id = serializers.UUIDField()
    initiative_type_id = serializers.UUIDField()


class InitiativeOutputSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    initiative_type = InitiativeTypeSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Initiative
        fields = [
            'id', 'title', 'description', 'current_stage', 'status', 'initiative_type',
            'category', 'owner', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'current_stage', 'status',
            'owner', 'created_at', 'updated_at'
        ]


class StageRequirementTemplateOutputSerializer(serializers.ModelSerializer):
    initiative_type = InitiativeTypeSerializer(read_only=True)
    class Meta:
        model = StageRequirementTemplate
        fields = [
            'id', 'initiative_type', 'stage', 'is_required',
            'document_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class StageRequirementTemplateInputSerializer(serializers.Serializer):
    initiative_type_id = serializers.UUIDField()
    stage = serializers.ChoiceField(choices=STAGES.choices)
    is_required = serializers.BooleanField(default=True)
    document_name = serializers.CharField(max_length=225)


class InitiativeDocumentOutputSerializer(serializers.ModelSerializer):
    initiative = InitiativeOutputSerializer(read_only=True)
    submitted_by = UserSerializer(read_only=True)
    class Meta:
        model = InitiativeDocument
        fields = [
            'id', 'initiative', 'stage', 'status', 'document_name', 'is_required',
            'submitted_by', 'submitted_at', 'waiver_reason'
        ]
        read_only_fields = [
            'id', 'submitted_by', 'submitted_at', 'created_at', 'updated_at'
        ]


class InitiativeDocumentInputSerializer(serializers.Serializer):
    initiative_id = serializers.UUIDField()
    stage = serializers.ChoiceField(choices=STAGES.choices)
    document_name = serializers.CharField(max_length=100)
    is_required = serializers.BooleanField(default=True)
    waiver_reason = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False
    )