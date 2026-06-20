from rest_framework.urls import path

from api.core.views.initiatives import GetAllInitiativeDocuments, CreateInitiativeType, ListAllInitiativeTypes, \
    GetInitiativeType

urlpatterns = [
    path('documents/all', GetAllInitiativeDocuments.as_view(), name='get_all_initiative_documents'),
    path('initiative_types/create', CreateInitiativeType.as_view(), name='create_initiative_type'),
    path('initiative_types/all', ListAllInitiativeTypes.as_view(), name='get_all_initiative_types'),
    path('initiative_types/<uuid:type_id>', GetInitiativeType.as_view(), name='get_initiative_type'),
]