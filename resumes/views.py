from typing import Optional

from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from resumes.dtos import ResumeDto
from resumes.models import Resume


class ResumesApiView(APIView):
    def get(self, request, resume_id):
        resume: Optional[Resume] = Resume.objects.filter(id=resume_id).first()
        if not resume:
            raise Http404(f"Resume with {id} not found")

        resume_dto = ResumeDto.from_orm(resume)

        print(resume_dto.dict())

        return JsonResponse(data=resume_dto.dict(), status=status.HTTP_200_OK)

    def patch(self, request, resume_id):
        resume_dto = ResumeDto(**request.data)
        Resume.objects.filter(id=resume_id).update(**resume_dto.dict(exclude_none=True))

        resume = Resume.objects.filter(id=resume_id).first()
        if not resume:
            raise Http404(f"Resume with {id} not found")

        resume_dto = ResumeDto.from_orm(resume)

        return JsonResponse(data=resume_dto.dict(), status=status.HTTP_202_ACCEPTED)
