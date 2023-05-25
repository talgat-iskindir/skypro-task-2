from django.contrib.auth import get_user_model
from django.db import models

from resumes.constants import RESUME_STATUSES, RESUME_CLOSE_STATUS, GRADES


class Resume(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(
        max_length=32, choices=RESUME_STATUSES, default=RESUME_CLOSE_STATUS
    )
    grade = models.CharField(max_length=32, choices=GRADES)
    specialty = models.TextField()
    salary = models.IntegerField()
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.TextField()
    title = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    email = models.EmailField()


class ResumeOwner(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = [["resume", "owner"]]

