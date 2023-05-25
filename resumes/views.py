from typing import Optional

from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from resumes.dtos import ResumeDto
from resumes.models import Resume


class ResumesApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, resume_id):
        resume: Optional[Resume] = Resume.objects.filter(id=resume_id).first()
        if not resume:
            return JsonResponse(
                data={"error": f"Resume with ID {resume_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        resume_dto = ResumeDto.from_orm(resume)

        return JsonResponse(data=resume_dto.dict(), status=status.HTTP_200_OK)

    def patch(self, request, resume_id):
        resume = Resume.objects.filter(id=resume_id).first()
        if not resume:
            return JsonResponse(
                data={"error": f"Resume with ID {resume_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not resume.owner or request.user.id != resume.owner.id:
            return JsonResponse(
                data={"error": f"Permission denied for resume with ID {resume_id}"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        resume_dto = ResumeDto(**request.data)
        Resume.objects.filter(id=resume_id).update(**resume_dto.dict(exclude_none=True))

        resume.refresh_from_db()
        resume_dto = ResumeDto.from_orm(resume)

        return JsonResponse(data=resume_dto.dict(), status=status.HTTP_202_ACCEPTED)
