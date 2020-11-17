from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list



# Create your models here.
class User(models.Model):
    mturk_id = models.TextField()
    
    consentAgreed = models.BooleanField(default=False)
    instrEnded = models.BooleanField(default=False)
    start_image_id = models.IntegerField(default=0)
    step = models.IntegerField(default=0)

    joinTime = models.DateTimeField(auto_now_add=True)
    consentEndTime = models.DateTimeField(default=timezone.now)
    instrEndTime = models.DateTimeField(default=timezone.now)

    def step_up(self):        
        self.step += 1
        self.save()

    def consentEnd(self):
        self.consentAgreed = True
        self.consentEndTime = timezone.now()
        self.save()

    def startTask(self, valid_usrs):
        self.instrEnded = True
        self.instrEndTime = timezone.now()
        self.start_image_id = (valid_usrs // 4) * 20
        self.save()

class Log(models.Model):
    class BehaviorTypes(models.TextChoices):
        null = 'NL', _('NULL')
        selectBox = 'SB', _('SelectBox')
        unselectBox = 'UB', _('UnselectBox')
        unselectAllBox = 'UA', _('UnselectAllBox')
        
        chooseLabel = 'CL', _('ChooseLabel')

        removeAnnotation = 'RA', _('RemoveAnnotation')
        removeAllAnnotation = 'RL', _('RemoveAllAnnotation')

        readInstruction = 'RI', _('ReadInstruction')
        submit = 'SU', _('Submit')

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    logTime = models.DateTimeField(auto_now_add=True)
    imageID = models.IntegerField(default=-1)
    boxIDs = models.TextField(default=[], validators=[validate_comma_separated_integer_list])
    label = models.CharField(max_length = 255)
    behavior = models.CharField(
        max_length = 2,
        choices = BehaviorTypes.choices,
        default=BehaviorTypes.null
    )

class Label(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    imageID = models.IntegerField()
    groupID = models.IntegerField()
    boxIDs = models.TextField(validators=[validate_comma_separated_integer_list])
    label = models.CharField(max_length = 255)


