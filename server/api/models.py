from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list



# Create your models here.
class User(models.Model):
    mturk_id = models.TextField()
    
    consentAgreed = models.BooleanField(default=False)
    step = models.IntegerField(default=1)

    joinTime = models.DateTimeField(auto_now_add=True)
    consentEndTime = models.DateTimeField(default=timezone.now)
    instrEndTime = models.DateTimeField(default=timezone.now)

    def step_up(self):        
        self.step += 1
        self.save()

    def instrEnd(self):
        self.instrEndTime = timezone.now()
        self.save()

    def consentEnd(self):
        self.consentAgreed = True
        self.consentEndTime = timezone.now()
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

    
    ImageID = models.IntegerField()
    boxIDs = models.TextField(validators=[validate_comma_separated_integer_list])
    behavior = models.CharField(
        max_length = 2,
        choices = BehaviorTypes.choices,
        default=BehaviorTypes.null
    )
