from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import ordinal
from .. import validators
from .. import utils
from .essentials import EventManager, AssignmentManager
USER = get_user_model()
DEPARTMENT_CHOICES = (
    ("csit", "BSc Computer Science and Information Technology"),
    ("bca", "Bachelor of Computer Application"),
    ("coer", "Computer Engineering"),
    ("eer", "Electrical Engineering"),
    ("mer", "Mechanical Engineering"),
    ("cer", "Civil Engineering")
)
STATUS_CHOICES = (
    (
        ("p", "Pending"),
        ("c", "Checked"),
        ("r", "Rejected"),
    )
)
DAYS_OF_WEEK = (
    ("sun", "Sunday"),
    ("mon", "Monday"),
    ("tue", "Tuesday"),
    ("wed", "Wednesday"),
    ("thu", "Thursday"),
    ("fri", "Friday")
)
ATTENDENCE_STATUS = (
    (
        "p", "Present"
    ),
    (
        "a", "Absent"
    )
)


class College(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to="images/logo/", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "College"


class Department(models.Model):
    name = models.CharField(choices=DEPARTMENT_CHOICES,
                            max_length=4, db_index=True)
    hod = models.OneToOneField(USER, on_delete=models.SET_NULL,
                               related_name="department", related_query_name="has_department", null=True,
                               validators=[validators.validate_teacher, ])

    def __str__(self):
        return f"Department of {self.get_name_display()}"


class Semester(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name="semester", related_query_name="has_semester")
    year = models.IntegerField(
        validators=[validators.validate_year, ], db_index=True)
    room = models.CharField(max_length=5, db_index=True)
    cr = models.OneToOneField(USER, on_delete=models.SET_NULL,
                              related_name="+", null=True, related_query_name="+", validators=[validators.validate_student, ]
                              )

    def __str__(self):
        return f"{self.department.get_name_display()} - {ordinal(timezone.now().date().year - self.year + 1)} year"


class Routine(models.Model):
    teacher = models.ForeignKey(USER, on_delete=models.CASCADE,
                                related_name="routine", related_query_name="has_routine")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,
                                 related_name="routine", related_query_name="has_routine")
    starts = models.TimeField()
    ends = models.TimeField()
    day_of_week = models.CharField(
        choices=DAYS_OF_WEEK, max_length=3, db_index=True)
    created_at = models.DateField(default=timezone.now, editable=False)
    updated_at = models.DateField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.semester} - {self.get_day_of_week_display()}"

    class Meta:
        ordering = ("starts",)


class Attendence(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL,
                                related_name="attendence", related_query_name="has_attendence", null=True, db_index=True)
    student = models.ForeignKey(USER, on_delete=models.CASCADE,
                                related_name='attendence', related_query_name="has_attendence", db_index=True)
    status = models.CharField(choices=ATTENDENCE_STATUS, max_length=1)
    date = models.DateField(default=timezone.now,
                            editable=False, db_index=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"{self.student.get_full_name()} {'is' if self.date == timezone.now().date() else 'was'} {self.get_status_display()} on {self.date}"


class Assignment(models.Model):
    topic = models.CharField(max_length=100, db_index=True)
    semester = models.ForeignKey(Semester,
                                 on_delete=models.CASCADE,
                                 related_name="assignment",
                                 related_query_name="has_assignment")
    description = models.TextField(null=True)
    upload = models.FileField(
        upload_to=utils.upload_directory_path, null=True, blank=True)
    teacher = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="+", related_query_name="+", validators=[validators.validate_teacher, ])
    submitted_by = models.ManyToManyField(
        USER, related_name="assignment", through="SubmittedBy", related_query_name="has_assignment")
    objects = AssignmentManager()
    due_date = models.DateField(db_index=True)
    assigned_at = models.DateField(default=timezone.now, editable=False)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ("due_date",)
        constraints = [
            models.UniqueConstraint(
                "topic", "semester", "teacher", name="unique_semester_topic_teacher"),
        ]


class SubmittedBy(models.Model):
    student = models.ForeignKey(USER, on_delete=models.CASCADE, validators=[
                                validators.validate_student, ])
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1, default="p")
    submitted_at = models.DateField(default=timezone.now, editable=False)

    class Meta:
        ordering = ("submitted_at",)


class Event(models.Model):
    topic = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/events/%Y-%m-%d")
    description = models.TextField()
    happening = models.DateTimeField()
    added_at = models.DateTimeField(default=timezone.now, editable=False)
    objects = EventManager()

    def __str__(self):
        return self.topic


class Club(models.Model):
    name = models.CharField(max_length=100)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    discord_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    president = models.OneToOneField(
        USER, on_delete=models.CASCADE, related_name="+", related_query_name="+")
    members = models.ManyToManyField(
        USER, related_name="club", related_query_name="has_club")

    def __str__(self):
        return self.name


class Discussion(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE,
                             related_name="discussion", related_query_name="has_discussion")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,
                                 related_name="discussion", related_query_name="has_discussion")
    message = models.TextField()
    discussed_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ("discussed_at",)
