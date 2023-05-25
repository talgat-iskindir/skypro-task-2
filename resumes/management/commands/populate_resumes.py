from django.core.management import BaseCommand

from resumes.models import Resume

resumes = [
    {
        "id": 10,
        "status": "RESUME_OPEN_STATUS",
        "grade": "GRADE_JUNIOR",
        "specialty": "Backend",
        "salary": 100000,
        "education": "Harvard",
        "experience": "SkyPro",
        "portfolio": "https://www.best-teacher.com",
        "title": "John Smith",
        "phone": "+123456789",
        "email": "john.smith@skypro.com",
    }
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for resume in resumes:
            resume, created = Resume.objects.get_or_create(**resume)
