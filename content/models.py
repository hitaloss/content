from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=50)
    module = models.TextField(max_length=None)
    students = models.PositiveIntegerField()
    description = models.TextField(null=True)
    is_active = models.BooleanField(null=True, default=False)

    def __repr__(self) -> str:
        return f"<[{self.id}] {self.title} - {self.module}>"
