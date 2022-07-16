from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
USER = get_user_model()


def validate_year(value):
    current_year = timezone.now().date().year
    if (current_year - value) <= 3:
        return
    raise ValidationError(
        _(f'Year must be in range {current_year - 3} - {current_year}')
    )


def validate_student(value):
    user = USER.objects.get(pk=value)
    if user.is_teacher:
        raise ValidationError(
            _("%(name)s ain't student", ), params={"name": user.get_full_name()}
        )


def validate_teacher(value):
    user = USER.objects.get(pk=value)
    if not user.is_teacher:
        raise ValidationError(
            _("%(name)s ain't teacher", ), params={"name": user.get_full_name()}
        )
