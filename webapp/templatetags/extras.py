from django import template
from ..models import SubmittedBy
register = template.Library()

@register.filter
def assgmentStatus(student,assignment):
    try:
        return SubmittedBy.objects.get(assignment=assignment,student=student).get_status_display()
    except SubmittedBy.DoesNotExist:
        return "Not Submitted"