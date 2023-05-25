from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from resumes.dtos import ResumeDto
from resumes.models import Resume


class ResumesApiViewTests(TestCase):
    def setUp(cls):
        cls.user = get_user_model().objects.create(
            username="testuser", password="12345", email="user@test.com"
        )
        cls.resume_data = {
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
        cls.resume = Resume.objects.create(**cls.resume_data)
        cls.patch_data = {
            "specialty": "Frontend",
        }

    def test_get_when_resume_does_not_exist(self):
        # Given
        url = reverse("resume", kwargs={"resume_id": 1})

        # When
        response = self.client.get(url, {}, content_type="application/json")

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_ok(self):
        # Given
        url = reverse("resume", kwargs={"resume_id": 10})

        # When
        response = self.client.get(url, {}, content_type="application/json")

        # Then
        expected_data = ResumeDto(**self.resume_data).dict()
        assert response.json() == expected_data
        assert response.status_code == status.HTTP_200_OK

    def test_patch_when_not_authenticated(self):
        # Given
        url = reverse("resume", kwargs={"resume_id": 10})

        # When
        response = self.client.patch(
            url, self.patch_data, content_type="application/json"
        )

        # Then
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_when_resume_does_not_exist(self):
        # Given
        self.client.force_login(self.user)
        url = reverse("resume", kwargs={"resume_id": 1})

        # When
        response = self.client.patch(
            url, self.patch_data, content_type="application/json"
        )

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_when_not_authorized(self):
        # Given
        self.client.force_login(self.user)
        url = reverse("resume", kwargs={"resume_id": 10})

        # When
        response = self.client.patch(
            url, self.patch_data, content_type="application/json"
        )

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_ok(self):
        # Given
        self.client.force_login(self.user)
        Resume.objects.filter(id=self.resume.id).update(owner=self.user)
        url = reverse("resume", kwargs={"resume_id": 10})

        # When
        response = self.client.patch(
            url, self.patch_data, content_type="application/json"
        )

        # Then
        expected_data = self.resume_data.copy()
        expected_data.update(**self.patch_data)
        assert response.json() == ResumeDto(**expected_data).dict()
        assert response.status_code == status.HTTP_202_ACCEPTED
