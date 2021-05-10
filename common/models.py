from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonInfo(models.Model):
    """
    common info that is frequently to be used in every model
    """

    created_on = models.DateTimeField("Created at", auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )
    modified_on = models.DateTimeField("Last modified at", auto_now=True, db_index=True)

    class Meta:
        abstract = True
