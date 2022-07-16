from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Discussion


class Login(UserPassesTestMixin, LoginView):
    template_name = "webapp/login.html"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("app_webapp:home"))


class Logout(LoginRequiredMixin, LogoutView):
    pass


class DiscussionView(LoginRequiredMixin,CreateView):
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
