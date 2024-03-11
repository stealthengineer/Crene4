from django.urls import path

from .views import (AddBranch,
                    BranchView,
                    BranchDetail,
                    LeafView)

urlpatterns = [
    path('createbranch/',AddBranch.as_view()),
    path('',BranchView.as_view(),name='branchview'),
    path('detail/<int:id>/',BranchDetail.as_view(),name='branch_detail'),
    path('leaf/',LeafView.as_view(),name='leaf')
]