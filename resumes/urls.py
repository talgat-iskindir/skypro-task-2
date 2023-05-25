from django.urls import path

from resumes.views import ResumesApiView

urlpatterns = [
    path("resumes/<int:resume_id>/", ResumesApiView.as_view(), name="resume"),
]
