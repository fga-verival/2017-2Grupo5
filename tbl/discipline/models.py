from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import Teacher


class Discipline(models.Model):
    """
    Class that manages the disciplines part of TBL.
    """

    title = models.CharField(
        _("Title"),
        max_length=100,
        help_text=_("Title of discipline")
    )

    course = models.CharField(
        _("Course"),
        max_length=100,
        help_text=_("Course that is ministered the discipline")
    )

    description = models.TextField(
        _("Description"),
        help_text=_("Description of discipline")
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="disciplines",
        related_query_name="discipline"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Discipline")
        verbose_name_plural = _("Disciplines")
