from django.shortcuts import render
from FacultyView.models import Student, AttendanceLog
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import uuid

# Create your views here.

present = set()


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_manually_post(request):
    if request.method == "POST":
        student_roll = request.POST.get("student-name")
        
        try:
            student = Student.objects.get(s_roll=student_roll)
            ip_address = get_client_ip(request)
            
            # Check if student can mark attendance (IP and time validation)
            can_mark, message = AttendanceLog.can_mark_attendance(student, ip_address)
            
            if not can_mark:
                # Store error message and redirect to error page
                request.session['error_message'] = message
                return HttpResponseRedirect("/attendance_error")
            
            # Generate or get session ID
            session_id = request.session.get('attendance_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['attendance_session_id'] = session_id
            
            # Log the attendance
            AttendanceLog.objects.create(
                student=student,
                ip_address=ip_address,
                session_id=session_id
            )
            
            # Add to present set for display
            present.add(student)
            
            return HttpResponseRedirect("/submitted")
            
        except Student.DoesNotExist:
            request.session['error_message'] = "Student not found."
            return HttpResponseRedirect("/attendance_error")
    
    return HttpResponseRedirect("/add_manually")


def submitted(request):
    return render(request, "StudentView/Submitted.html")


def attendance_error(request):
    error_message = request.session.get('error_message', 'An error occurred.')
    # Clear the error message after retrieving it
    if 'error_message' in request.session:
        del request.session['error_message']
    return render(request, "StudentView/AttendanceError.html", {'error_message': error_message})
