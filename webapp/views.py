from ast import Sub
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, list, detail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from .models import Discussion, Assignment, Submission, Event
from django.db.models import Q


class Login(UserPassesTestMixin, LoginView):
    template_name = "webapp/login.html"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("app_webapp:dashboard"))


class Logout(LoginRequiredMixin, LogoutView):
    pass


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "webapp/index.html"

    def get(self, request, *args, **kwargs):
        today = timezone.now().date().strftime("%a").lower()
        today = "sun" if today == "sat" else today
        user = request.user
        if not user.is_teacher:
            context = {
                "routines": user.semester.routine.filter(day_of_week=today),
                "remaining_assignments": user.semester.assignment.all().get_upcoming()

            }
        else:
            context = {
                "routines": user.routine.filter(day_of_week=today),
                "assignments": Submission.objects.filter(assignment__teacher=user, status="p")
            }
            self.template_name = "webapp/teacher_index.html"
        return render(request, self.template_name, context)


class AssignmentView(LoginRequiredMixin, list.ListView):
    model = Assignment
    template_name = "webapp/assignment.html"
    context_object_name = "assignments"

    def get_queryset(self):
        return super().get_queryset().filter(semester=self.request.user.semester)


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = "webapp/homework.html"
    fields = ("assignment",)
    success_url = reverse_lazy("app_webapp:assignment")

    def get(self, request, pk):
        return render(request, self.template_name, {"assignment": Assignment.objects.get(id=pk)})

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class DiscussionView(LoginRequiredMixin, CreateView):
    template_name = "webapp/discussion.html"
    model = Discussion
    fields = ("message",)
    success_url = reverse_lazy("app_webapp:discussion")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"discussions": self.request.user.semester.discussion.all()[:20]})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.semester = self.request.user.semester
        return super().form_valid(form)


class EventView(LoginRequiredMixin, list.ListView):
    template_name = "webapp/events.html"
    model = Event
    context_object_name = "events"

    def get_queryset(self):
        return super().get_queryset().filter(happening__date__gte=timezone.now())

class AttendenceView(LoginRequiredMixin,TemplateView):
    template_name = "webapp/attendence.html"