from rest_framework.urls import path

from api.core.views.initiatives import GetAllInitiativeDocuments, InitiativeTypeListCreateView, \
    InitiativeTypeDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('documents/all', GetAllInitiativeDocuments.as_view(), name='get_all_initiative_documents'),
    path('initiative_types', InitiativeTypeListCreateView.as_view(), name='initiative_type_list_create'),
    path('initiativetypes/<uuid:type_id>', InitiativeTypeDetailView.as_view(), name='initiative_type_detail_view'),
    path('categories', CategoryListCreateView.as_view(), name='category_list_create_view'),
    path('categories/<uuid:category_id>', CategoryDetailView.as_view(), name='category_detail_view'),
]