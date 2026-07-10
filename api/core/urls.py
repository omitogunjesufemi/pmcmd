from rest_framework.urls import path

from api.core.views.initiatives import InitiativeTypeListCreateView, \
    InitiativeTypeDetailView, CategoryListCreateView, CategoryDetailView, RequirementTemplateListCreateView, \
    RequirementTemplateDetailView, InitiativeListCreateView, InitiativeDetailUpdateView, \
    InitiativeDocumentListView, InitiativeDocumentDetailView, OwnerInitiativeDocumentListView, \
    PendingApprovalsInitiativeDocumentListView, DocumentsForAInitiativeListView, \
    BlockingDocumentsForInitiativeView, SubmitDocumentForInitiativeView, AdvanceInitiativeStageView

urlpatterns = [
    path('initiatives', InitiativeListCreateView.as_view(), name='initiative_list_create_view'),
    path('initiatives/<uuid:initiative_id>', InitiativeDetailUpdateView.as_view(), name='initiative_detail_update'),
    path('initiatives/<uuid:initiative_id>/advance-stage', AdvanceInitiativeStageView.as_view(), name='advance_initiative_stage'),

    path('initiative_types', InitiativeTypeListCreateView.as_view(), name='initiative_type_list_create'),
    path('initiativetypes/<uuid:type_id>', InitiativeTypeDetailView.as_view(), name='initiative_type_detail_view'),

    path('initiatives/owner/documents', OwnerInitiativeDocumentListView.as_view(), name='documents_for_owner'),
    path('initiative/documents/pending_approval', PendingApprovalsInitiativeDocumentListView.as_view(),
         name='documents_pending_approval_for_initiative'),
    path('initiative/documents/blocking', BlockingDocumentsForInitiativeView.as_view(),
         name='documents_pending_upload_for_initiative'),
    path('initiative/documents/<uuid:initiative_id>', DocumentsForAInitiativeListView.as_view(),
         name='documents_for_an_initiative'),
    path('initiative_documents', InitiativeDocumentListView.as_view(), name='initiative_document_list'),
    path('initiative_documents/<uuid:document_id>', InitiativeDocumentDetailView.as_view(),
         name='initiative_document_detail'),
    path('initiatives/<uuid:initiative_id>/submit_document', SubmitDocumentForInitiativeView.as_view(), name='submit_document_for_initiative'),

    path('categories', CategoryListCreateView.as_view(), name='category_list_create_view'),
    path('categories/<uuid:category_id>', CategoryDetailView.as_view(), name='category_detail_view'),
    path('required_templates', RequirementTemplateListCreateView.as_view(), name='requirement_template_list_create'),
    path('required_templates/<uuid:template_id>', RequirementTemplateDetailView.as_view(),
         name='requirement_template_detail'),
]
