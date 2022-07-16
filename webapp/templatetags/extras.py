from django import template
from ..models import Submission
register = template.Library()

@register.filter
def assgmentStatus(student,assignment):
    sub = Submission.objects.filter(assignment=assignment,student=student).first()
    if sub:
        return sub.get_status_display()
    return "Not Submitted"