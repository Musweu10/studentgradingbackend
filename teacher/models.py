# teacher/models.py
from django.utils import timezone
from django.db import models
import uuid
from django.conf import settings


class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='class_students',
        limit_choices_to={'role': 'student'}
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    class_assigned = models.ForeignKey('Class', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.class_assigned.name})"


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_assigned = models.ForeignKey('Class', on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('class_assigned', 'student', 'date')
        ordering = ['-date']  # Order by most recent date


class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    mid_term_score = models.FloatField()
    final_exam_score = models.FloatField()
    total_score = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate total score when saving
        self.total_score = (self.mid_term_score + self.final_exam_score) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Grade for {self.student.get_full_name()} in {self.subject.name}"
