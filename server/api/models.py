from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list



# Create your models here.
class User(models.Model):
    username= models.TextField()
    
    consentAgreed = models.BooleanField(default=False)
    instrEnded = models.BooleanField(default=False)
    # start_image_id = models.IntegerField(default=0)
    # step = models.IntegerField(default=0)

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
        self.start_image_id = 0
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


class DocType(models.Model):
    doctype=models.CharField(max_length=250)
    def __str__(self):
        return self.doctype

class Document(models.Model):
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    doc_no=models.IntegerField(default=999)
    def __str__(self):
        return self.doctype.doctype+"-"+str(self.doc_no)

class InitCat(models.Model):
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    cat_no=models.IntegerField()
    cat_text=models.CharField(max_length=255)
    def __str__(self):
        return self.doctype.doctype+"-"+str(self.cat_no)+'-'+str(self.cat_text)


class InitSubCat(models.Model):
    initcat=models.ForeignKey('InitCat', on_delete=models.CASCADE)
    subcat_no=models.IntegerField()
    subcat_text=models.CharField(max_length=255)
    subcat_description=models.CharField(max_length=255)
    def __str__(self):
        return str(self.subcat_no)+'-'+str(self.subcat_text)


class UserCat(models.Model):
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    cat_no=models.IntegerField()
    cat_text=models.CharField(max_length=255)
    def __str__(self):
        return self.user.username+'-'+self.doctype.doctype+"-"+str(self.cat_no)+'-'+str(self.cat_text)

class UserSubcat(models.Model):
    usercat=models.ForeignKey('UserCat', on_delete=models.CASCADE)
    subcat_no=models.IntegerField()
    subcat_text=models.CharField(max_length=255)
    subcat_description=models.CharField(max_length=255)
    def __str__(self):
        return self.usercat.user.username+'-'+str(self.subcat_no)+'-'+str(self.subcat_text)

class Annotation(models.Model):
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    doc_no=models.IntegerField(default=1)
    box_id=models.IntegerField(default=1)
    status=models.BooleanField(default=False)
    label=models.ForeignKey('UserSubcat', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.user.username+'-'+str(self.doc_no)+'-'+str(self.box_id)+'-'+self.label

class Status(models.Model):
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    document=models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+'-'+self.document+'-'+str(self.status)


