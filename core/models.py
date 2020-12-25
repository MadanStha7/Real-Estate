from django.db import models




class FieldVisit(models.Model):

    name=models.CharField(max_length=30)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    property=models.ManyToManyField(Property)

    def __str__(self):
        return  (self.name)

    class Meta:
        ordering=['name']
        db_table = 'fieldvisit_form'


