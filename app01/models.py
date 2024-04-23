from django.db import models


# Create your models here.
class Department(models.Model):
    """department table"""
    title = models.CharField(verbose_name='title', max_length=32)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """staff table"""
    name = models.CharField(verbose_name="name", max_length=16)
    password = models.CharField(verbose_name="password", max_length=64)
    age = models.IntegerField(verbose_name='age')
    account = models.DecimalField(verbose_name='balance', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='create time')

    # cascade
    depart = models.ForeignKey(verbose_name='department', to='Department', to_field='id', on_delete=models.CASCADE)
    # set null
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    # constraints in django
    gender_choices = (
        (1, 'male'),
        (2, 'female'),
    )

    gender = models.SmallIntegerField(verbose_name='gender', choices=gender_choices)

class PrettyNum(models.Model):
    """pretty number"""
    mobile = models.CharField(verbose_name='phone number', max_length=11)
    # if allow null, null = True, blank = True
    price = models.IntegerField(verbose_name='price', default=0)

    level_choices = (
        (1, 'level 1'),
        (2, 'level 2'),
        (3, 'level 3'),
        (4, 'level 4'),
    )

    level = models.SmallIntegerField(verbose_name='level', choices=level_choices, default=1)

    status_choices = (
        (1, 'occupied'),
        (2, 'unoccupied'),
    )

    status = models.SmallIntegerField(verbose_name='status', choices=status_choices, default=2)