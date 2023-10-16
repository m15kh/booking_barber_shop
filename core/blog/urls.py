from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path("", PostViewList.as_view(), name = "all_post" ),
    path("<int:pk>/", PostViewDetail.as_view(), name = "detail_post" ),
    path("new/", PostViewNew.as_view(), name = "new_post" ),
    path("<int:pk>/edit/", PostViewEdit.as_view(), name = "edit_post" ),
    path("<int:pk>/delete/", PostViewDelete.as_view(), name = "delete_post" ),
    
]

