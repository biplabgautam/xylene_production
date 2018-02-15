from django.db import models
from cms.models import Subject, Chapter, Subtopic
from django.urls import reverse
from django.contrib.auth.models import User

#For slug field
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

#Upload path for saq, numerical images
def image_upload(instance, filename):
	if isinstance(instance, TempSAQ):
		return '{0}/{1}/saqs/{2}'.format(instance.chapter.subject.subject_name, instance.chapter.chapter_name, filename)
	elif isinstance(instance, TempNumerical):
		return '{0}/{1}/numericals/{2}'.format(instance.chapter.subject.subject_name, instance.chapter.chapter_name, filename)
	elif isinstance(instance, TempSubsectionImage):
		return '{0}/{1}/{2}/{3}'.format(instance.subtopic.chapter.subject.subject_name, instance.subtopic.chapter.chapter_name, instance.subtopic.title, filename)

class TempSubsection(models.Model):
	subsection_serial = models.IntegerField(null=False)
	title = models.CharField(max_length=360)
	slug = models.SlugField(unique=True, blank=True)
	content = models.TextField()
	subtopic = models.ForeignKey('cms.Subtopic', on_delete=models.CASCADE)
	remarks = models.CharField(max_length=360, blank=True, help_text = "For example: HSEB 2068, HSEB 2070 Frequently asked in Entrance, etc.")
	date_modified = models.DateField(auto_now=True, auto_now_add=False) #For the date of last modification
	#An integer field which stores the id of the content being edited 
	temp_id = models.IntegerField(null=True, blank = True)
	#Boolean field which indicates whether the content was edited or created
	edited_bool = models.BooleanField(default = False)
	#User who last modified it
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'last_modified_by_tempsubsection')

	class Meta:
		ordering = ["subtopic", "-date_modified"]
		permissions = (
            ("view_pending_subsections", "Can see pending Subsection items"),
            ("approve_pending_subsections", "Can approve pending Subsection items"),
        )

	def __str__(self):
		return self.title

	def get_subsection_approval_url(self):
		return reverse("tcms:approve_subsection", kwargs = {"tempsubsec_pk":self.pk})
	#URL for a user to see submitted contents
	def get_tempsubsection_see_url(self):
		return reverse("accounts:see_tempsubsection", kwargs = {"tempsubsec_pk":self.pk})

class TempSAQ(models.Model):
	question_serial = models.IntegerField(null=False)
	slug = models.SlugField(unique=True, blank=True)
	question = models.TextField()
	answer = models.TextField()
	important = models.BooleanField(default = False)
	remarks = models.CharField(max_length=360, blank=True, help_text = "E.g. HSEB 2068, HSEB 2070 Frequently asked in Entrance, etc.")
	chapter = models.ForeignKey('cms.Chapter', on_delete=models.CASCADE)
	subtopic = models.ForeignKey('cms.Subtopic', on_delete=models.CASCADE, null=True, blank=True)
	date_modified = models.DateField(auto_now=True, auto_now_add=False) #For the date of last modification

	display_image = models.ImageField(upload_to = image_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	image_caption = models.CharField(max_length=300, blank=True)
	#An integer field which stores the id of the content being edited 
	temp_id = models.IntegerField(null=True, blank = True)
	#Boolean field which indicates whether the content was edited or created
	edited_bool = models.BooleanField(default = False)
	#User who last modified it
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'last_modified_by_tempSAQ')	
	
	class Meta:
		ordering = ["chapter", "-date_modified"]
		permissions = (
            ("view_pending_saqs", "Can see pending SAQ items"),
            ("approve_pending_saqs", "Can approve pending SAQ items"),
        )
	def __str__(self):
		string = "%s" %(self.question_serial)
		return string

	def get_saq_approval_url(self):
		return reverse("tcms:approve_saq", kwargs = {"tempsaq_pk":self.pk})
	#URL for a user to see submitted saqs
	def get_tempsaq_see_url(self):
		return reverse("accounts:see_tempsaq", kwargs = {"tempsaq_pk":self.pk})

class TempNumerical(models.Model):
	numerical_serial = models.IntegerField(null=False)
	slug = models.SlugField(unique=True, blank=True)
	question = models.TextField()
	answer = models.TextField()
	important = models.BooleanField(default = False)
	remarks = models.CharField(max_length = 360, blank=True, help_text = "For example: HSEB 2068, HSEB 2070 Frequently asked in Entrance, etc.")
	chapter = models.ForeignKey('cms.Chapter', on_delete=models.CASCADE)
	subtopic = models.ForeignKey('cms.Subtopic', on_delete=models.CASCADE, blank=True, null=True)

	date_modified = models.DateField(auto_now=True, auto_now_add=False) #For the date of last modification

	display_image = models.ImageField(upload_to = image_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	image_caption = models.CharField(max_length=300, blank=True)
	#An integer field which stores the id of the content being edited 
	temp_id = models.IntegerField(null=True, blank = True)
	#Boolean field which indicates whether the content was edited or created
	edited_bool = models.BooleanField(default = False)
	#User who last modified it
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'last_modified_by_tempNumerical')	
	
	class Meta:
		ordering = ["chapter", "-date_modified"]
		permissions = (
            ("view_pending_numericals", "Can see pending Numerical items"),
            ("approve_pending_numericals", "Can approve pending Numerical items"),
        )
	def __str__(self):
		string = "%s" %(self.numerical_serial)
		return string

	def get_numerical_approval_url(self):
		return reverse("tcms:approve_numerical", kwargs = {"tempnum_pk":self.pk})

	#URL for a user to see submitted numericals
	def get_tempnumerical_see_url(self):
		return reverse("accounts:see_tempnumerical", kwargs = {"tempnum_pk":self.pk})

class TempSubsectionImage(models.Model):
	image_serial = models.IntegerField(null=False)
	caption = models.CharField(max_length = 240, blank=True)
	slug = models.SlugField(unique = True,blank = True)

	image = models.ImageField(upload_to = image_upload, width_field = "width_field",
							height_field = "height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)

	date_modified = models.DateField(auto_now=True, auto_now_add=False) #For the date of last modification

	subsection = models.ForeignKey("cms.Subsection", on_delete=models.CASCADE)
	subtopic = models.ForeignKey("cms.Subtopic", on_delete = models.CASCADE)
	#An integer field which stores the id of the content being edited 
	temp_id = models.IntegerField(null=True, blank = True)
	#Boolean field which indicates whether the content was edited or created
	edited_bool = models.BooleanField(default = False)
	#User who last modified it
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'last_modified_by_tempSubsectionImage')	

	class Meta:
		ordering = ["subsection", "-date_modified"]
		permissions = (
            ("view_pending_subsection_images", "Can see pending Subsection Image items"),
            ("approve_pending_subsection_images", "Can approve pending Subsection Image items"),
        )
	
	def __str__(self):
		return self.caption

	def get_subsection_image_approval_url(self):
		return reverse("tcms:approve_subsection_image", kwargs = {"tempsubsecimg_pk":self.pk})

	#URL for a user to see submitted contents
	def get_tempsubsection_image_see_url(self):
		return reverse("accounts:see_tempsubsection_image", kwargs = {"tempsubsecimg_pk":self.pk})


def slugify_unique(value, model, slugfield="slug"):
        suffix = 0
        potential = base = slugify(value)
        while True:
            if suffix:
                potential = "-".join([base, str(suffix)])
            if not model.objects.filter(**{slugfield: potential}).count():
                return potential
            suffix += 1

def create_slug(instance, new_slug=None):
	if isinstance(instance, TempSubsection):
		slug = slugify_unique(instance.title, TempSubsection)
	elif isinstance(instance, TempSAQ):
		slug = slugify_unique('saq', TempSAQ)
	elif isinstance(instance, TempNumerical):
		slug = slugify_unique('numerical', TempNumerical)
	elif isinstance(instance, TempSubsectionImage):
		slug = slugify_unique(instance.caption, TempSubsectionImage)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=TempSubsection)
pre_save.connect(pre_save_post_receiver, sender=TempSAQ)
pre_save.connect(pre_save_post_receiver, sender=TempNumerical)
pre_save.connect(pre_save_post_receiver, sender=TempSubsectionImage)