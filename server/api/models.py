from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='', null=True, blank=True)
    is_done = models.BooleanField(default=True)

class Box(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    parent = models.IntegerField() # id
    child = models.IntegerField() # id
    left_top_x = models.IntegerField(validators=[MaxValueValidator(256), MinValueValidator(0)])
    left_top_y = models.IntegerField(validators=[MaxValueValidator(256), MinValueValidator(0)])
    width = models.IntegerField(validators=[MaxValueValidator(256), MinValueValidator(0)])
    height = models.IntegerField(validators=[MaxValueValidator(256), MinValueValidator(0)])


class Taxonomy(models.Model):
    pass

# Taxonomy not Implemented.
# Box group Not Implemented.