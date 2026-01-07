from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.utils import timezone
from datetime import timedelta


class Section(models.Model):
    section = models.CharField(max_length=2)

    def __str__(self) -> str:
        return self.section


class Year(models.Model):
    year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )

    def __str__(self) -> str:
        return str(self.year)


class Branch(models.Model):
    branch = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.branch


class Student(models.Model):
    s_roll = models.CharField(max_length=20, primary_key=True)
    s_fname = models.CharField(max_length=20)
    s_lname = models.CharField(max_length=20)
    s_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    s_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    s_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.s_fname} {self.s_lname} - {self.s_roll} - {self.s_branch}({self.s_year}{self.s_section})"


class AttendanceLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, default="")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"{self.student.s_roll} - {self.ip_address} - {self.timestamp}"

    @staticmethod
    def can_mark_attendance(student, ip_address):
        """Check if student can mark attendance based on IP and time restrictions"""
        now = timezone.now()
        two_hours_ago = now - timedelta(hours=2)
        
        # Check if student marked attendance in last 2 hours
        recent_student_attendance = AttendanceLog.objects.filter(
            student=student,
            timestamp__gte=two_hours_ago
        ).exists()
        
        if recent_student_attendance:
            return False, "You have already marked attendance. Please wait 2 hours before marking again."
        
        # Check if IP address was used in current session (prevent proxy)
        # Get current session's attendance (last 30 minutes considered as same session)
        session_time = now - timedelta(minutes=30)
        ip_used = AttendanceLog.objects.filter(
            ip_address=ip_address,
            timestamp__gte=session_time
        ).exists()
        
        if ip_used:
            return False, "This IP address has already been used to mark attendance. Proxy attendance is not allowed."
        
        return True, "OK"
