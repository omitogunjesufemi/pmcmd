from rest_framework.urls import path

from api.core.views.initiatives import GetAllInitiativeDocuments, InitiativeTypeListCreateView, \
    InitiativeTypeDetailView, CategoryListCreateView, CategoryDetailView, RequirementTemplateListCreateView, \
    RequirementTemplateDetailView, InitiativeListCreateView, InitiativeDetailUpdateView

urlpatterns = [
    path('initiatives', InitiativeListCreateView.as_view(), name='initiative_list_create_view'),
    path('initiatives/<uuid:initiative_id>', InitiativeDetailUpdateView.as_view(), name='initiative_detail_update'),
    path('initiative_types', InitiativeTypeListCreateView.as_view(), name='initiative_type_list_create'),
    path('initiativetypes/<uuid:type_id>', InitiativeTypeDetailView.as_view(), name='initiative_type_detail_view'),
    path('categories', CategoryListCreateView.as_view(), name='category_list_create_view'),
    path('categories/<uuid:category_id>', CategoryDetailView.as_view(), name='category_detail_view'),
    path('required_templates', RequirementTemplateListCreateView.as_view(), name='requirement_template_list_create'),
    path('required_templates/<uuid:template_id>', RequirementTemplateDetailView.as_view(), name='requirement_template_detail'),
]
