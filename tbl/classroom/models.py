from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from discipline.models import Discipline
from accounts.models import Student


def min_value_validated(value):
    """
    Verify if the student limit is not negative and not zero.
    """

    if value <= 0:
        raise ValidationError(
            _("%(value)s is not bigger than 0."),
            params={'value': value}
        )


class ClassRoom(models.Model):
    """
    Class that manages the classes from specific discipline.
    """

    title = models.CharField(
        _('Title'),
        max_length=100,
        help_text=_("Title of class")
    )

    password = models.CharField(
        _("Password"),
        max_length=20,
        help_text=_("Class access password")
    )

    student_limit = models.IntegerField(
        _("Student Limit"),
        help_text=_("Maximum number of students in the class"),
        validators=[min_value_validated]
    )

    is_closed = models.BooleanField(
        _("Is closed?"),
        default=False,
        help_text=_("Checks if class is closed")
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="classes",
        related_query_name="class"
    )

    students = models.ManyToManyField(
        Student,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("ClassRoom")
        verbose_name_plural = _("Classes")
        ordering = ('title',)
