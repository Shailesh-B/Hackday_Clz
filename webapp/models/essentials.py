from django.db import models
from django.utils import timezone


class AssignmentQuerySet(models.QuerySet):
    def get_upcoming(self):
        return self.filter(due_date__gte=timezone.now())

    def get_due_today(self):
        return self.filter(due_date=timezone.now())


class AssignmentManager(models.Manager):
    def get_queryset(self):
        return AssignmentQuerySet(self.model)


class EventQuerySet(models.QuerySet):
    def get_upcoming(self):
        return self.filter(happening__gte=timezone.now())

    def get_happening_today(self):
        return self.filter(happening=timezone.now())


class EventManager(models.Model):
    def get_queryset(self):
        return EventQuerySet(self.model)
