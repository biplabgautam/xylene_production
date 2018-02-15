from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

#For slug field
from django.db.models.signals import pre_save
from django.utils.text import slugify

#For imagekit
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

#Upload path for subject, chapter, subtopic poster images
def poster_upload(instance, filename):
	if isinstance(instance, Subject):
		return '{0}/{1}'.format(instance.subject_name, filename)
	elif isinstance(instance, Chapter):
		return '{0}/{1}/{2}'.format(instance.subject.subject_name, instance.chapter_name, filename)
	elif isinstance(instance, Subtopic):
		return '{0}/{1}/{2}/{3}'.format(instance.chapter.subject.subject_name, instance.chapter.chapter_name, instance.title, filename)

#Upload path for saq, numerical images
def image_upload(instance, filename):
	if isinstance(instance, SAQ):
		return '{0}/{1}/saqs/{2}'.format(instance.chapter.subject.subject_name, instance.chapter.chapter_name, filename)
	elif isinstance(instance, Numerical):
		return '{0}/{1}/numericals/{2}'.format(instance.chapter.subject.subject_name, instance.chapter.chapter_name, filename)

# Create your models here.

class Subject(models.Model):
	subject_name = models.CharField(max_length=120)
	slug = models.SlugField(unique=True, blank=True)
	faculty = models.CharField(max_length = 120, blank=True)
	grade = models.CharField(max_length = 120, blank = True, null=True)

	poster_image = models.ImageField(upload_to = poster_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")
	poster_thumbnail = ImageSpecField(source='poster_image',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 100})

	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)

	poster_text = models.CharField(max_length=300, blank=True)

	def get_subject_select_url(self):
		return reverse("cms:subject_select", kwargs={"sub_pk":self.pk})

	def get_subject_edit_url(self):
		return reverse("cms:subject_edit", kwargs={"sub_pk":self.pk})

	def get_chapter_create_url(self):
		return reverse("cms:chapter_create", kwargs={"sub_slug":self.slug})

	def __str__(self):
		return self.subject_name

class Chapter(models.Model):
	chapter_serial = models.IntegerField(null=False, help_text="Chapter No.")
	slug = models.SlugField(unique=True, blank=True)
	chapter_name = models.CharField(max_length=120)
	section = models.CharField(max_length = 120, blank=True)
	subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, blank=True)

	poster_image = models.ImageField(upload_to = poster_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")

	poster_text = models.CharField(max_length=300, blank=True)
	poster_thumbnail = ImageSpecField(source='poster_image',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 100})

	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)

	class Meta:
		ordering = ["chapter_serial"]

	def get_subject_select_from_chapter(self):
		""" This function was created to call the subject select url from a chapter instance. """
		subject_instance = self.subject
		return reverse("cms:subject_select", kwargs={"sub_pk":subject_instance.pk})

	def get_chapter_select_url(self):
		return reverse("cms:chapter_select", kwargs={"chap_slug":self.slug})

	def get_saq_list_url(self):
		return reverse("cms:saq_list", kwargs={"chap_slug":self.slug})

	def get_numerical_list_url(self):
		return reverse("cms:numerical_list", kwargs={"chap_slug":self.slug})

	def get_chapter_edit_url(self):
		return reverse("cms:chapter_edit", kwargs={"chap_slug":self.slug})

	def get_subtopic_create_url(self):
		return reverse("cms:subtopic_create", kwargs={"chap_slug":self.slug})

	def get_saq_create_url(self):
		return reverse("tcms:saq_create", kwargs={"chap_slug":self.slug})

	def get_numerical_create_url(self):
		return reverse("tcms:numerical_create", kwargs={"chap_slug":self.slug})


	def __str__(self):
		return self.chapter_name

#content class to contain the detailed material.
class Subtopic(models.Model):
	subtopic_serial = models.IntegerField(null=False)
	slug = models.SlugField(unique=True, blank=True)
	title = models.CharField(max_length=240)
	chapter = models.ForeignKey('Chapter', on_delete=models.SET_NULL, null=True, blank=True)
	remarks = models.CharField(max_length=360, blank=True)

	poster_image = models.ImageField(upload_to = poster_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")

	poster_text = models.CharField(max_length=300, blank=True)
	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)
	poster_thumbnail = ImageSpecField(source='poster_image',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 100})

	class Meta:
		ordering = ["chapter", "subtopic_serial"]

	def get_subtopic_select_url(self):
		return reverse("cms:subtopic_select", kwargs={"chap_slug":self.chapter.slug, "subt_slug":self.slug})

	def get_subtopic_edit_url(self):
		return reverse("cms:subtopic_edit", kwargs={"chap_slug":self.chapter.slug, "subt_pk":self.pk})

	def get_subsection_create_url(self):
		return reverse("tcms:subsection_create", kwargs={"chap_slug":self.chapter.slug, "subt_pk":self.pk})

	def get_subsection_image_create_url(self):
		return reverse("tcms:subsection_image_create", kwargs={"chap_slug":self.chapter.slug, "subt_pk":self.pk})

	def __str__(self):
		return self.title

#Class for each subsection of the subtopic
class Subsection(models.Model):
	subsection_serial = models.IntegerField(null=False)
	title = models.CharField(max_length=360)
	slug = models.SlugField(unique=True, blank=True)
	content = models.TextField()
	subtopic = models.ForeignKey('Subtopic', on_delete=models.CASCADE)
	remarks = models.CharField(max_length=360, blank=True)
	date_created = models.DateField(auto_now=False, auto_now_add=True) #For the date of creation
	date_modified = models.DateField() #For the date of last modification
	#User logs
	created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'created_by_subsection')
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'last_modified_by_subsection')
	approved_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'approved_by_subsection')

	class Meta:
		ordering = ["subsection_serial"]

	def __str__(self):
		return self.title

	def get_subsection_edit_url(self):
		return reverse("tcms:subsection_edit", kwargs={"chap_slug":self.subtopic.chapter.slug, "subt_pk":self.subtopic.pk, "subsec_pk":self.pk})

#Class for short answer questions
class SAQ(models.Model):
	question_serial = models.IntegerField(null=False)
	slug = models.SlugField(unique=True, blank=True)
	question = models.TextField()
	answer = models.TextField()
	important = models.BooleanField(default = False)
	remarks = models.CharField(max_length=360, blank=True)
	chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
	subtopic = models.ForeignKey('Subtopic', on_delete=models.CASCADE, null=True, blank=True)
	date_created = models.DateField(auto_now=False, auto_now_add=True) #For the date of creation
	date_modified = models.DateField() #For the date of last modification
	#User logs
	created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'created_by_saq')
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'last_modified_by_saq')
	approved_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'approved_by_saq')

	display_image = models.ImageField(upload_to = image_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")
	image_caption = models.CharField(max_length=300, blank=True)
	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)

	class Meta:
		ordering = ["question_serial"]

	def get_saq_select_url(self):
		return reverse("cms:saq_select", kwargs={"chap_slug":self.chapter.slug, "saq_pk":self.pk})

	def get_saq_edit_url(self):
		return reverse("tcms:saq_edit", kwargs={"chap_slug":self.chapter.slug, "saq_pk":self.pk})

	def __str__(self):
		string = "%s" %(self.question_serial)
		return string

#Class for numerical problems
class Numerical(models.Model):
	numerical_serial = models.IntegerField(null=False)
	slug = models.SlugField(unique=True, blank=True)
	question = models.TextField()
	answer = models.TextField()
	important = models.BooleanField(default = False)
	remarks = models.CharField(max_length = 360, blank=True)
	chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
	subtopic = models.ForeignKey('Subtopic', on_delete=models.CASCADE, blank=True, null=True)
	date_created = models.DateField(auto_now=False, auto_now_add=True) #For the date of creation
	date_modified = models.DateField() #For the date of last modification
	#User logs
	created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'created_by_numerical')
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'last_modified_by_numerical')
	approved_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'approved_by_numerical')

	display_image = models.ImageField(upload_to = image_upload, null=True, blank=True,
							width_field = "width_field",
							height_field = "height_field")

	image_caption = models.CharField(max_length=300, blank=True)

	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)

	class Meta:
		ordering = ["numerical_serial"]

	def get_numerical_select_url(self):
		return reverse("cms:numerical_select", kwargs={"chap_slug":self.chapter.slug, "num_pk":self.pk})

	def get_numerical_edit_url(self):
		return reverse("tcms:numerical_edit", kwargs={"chap_slug":self.chapter.slug, "num_pk":self.pk})

	def __str__(self):
		string = "%s" %(self.numerical_serial)
		return string

#Class for images inside a subtopic. These images are connected to specific subsections through foreignkey.
class SubsectionImage(models.Model):
	image_serial = models.IntegerField(null=False)
	caption = models.CharField(max_length = 240, blank=True)
	slug = models.SlugField(unique = True,blank = True)

	image = models.ImageField(width_field = "width_field",
							height_field = "height_field")
	height_field = models.IntegerField(default = 0, blank=True, null=True)
	width_field = models.IntegerField(default = 0, blank=True, null=True)

	image_thumbnail = ImageSpecField(source = 'image',
									processors = [ResizeToFill(400, 400)],
									format = 'png',
									options = {'quality': 100})

	date_created = models.DateField(auto_now=False, auto_now_add=True) #For the date of creation
	date_modified = models.DateField() #For the date of last modification

	subsection = models.ForeignKey("Subsection", on_delete = models.SET_NULL, blank=True, null=True, related_name = 'subsection_image')
	subtopic = models.ForeignKey("Subtopic", on_delete = models.SET_NULL, blank=True, null=True, related_name = 'subsection_image')
	#User logs
	created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'created_by_subsection_image')
	last_modified_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'last_modified_by_subsection_image')
	approved_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name = 'approved_by_subsection_image')

	class Meta:
		ordering = ["image_serial"]

	def __str__(self):
		return self.caption

	def get_subsection_image_edit_url(self):
		return reverse("tcms:subsection_image_edit", kwargs={"chap_slug":self.subtopic.chapter.slug, "subt_pk":self.subtopic.pk, "subsecimg_pk":self.pk})

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
	if isinstance(instance,Subject):
		slug = slugify_unique(instance.subject_name, Subject)
	elif isinstance(instance, Chapter):
		slug = slugify_unique(instance.chapter_name, Chapter)
	elif isinstance(instance, Subtopic):
		slug = slugify_unique(instance.title, Subtopic)
	elif isinstance(instance, Subsection):
		slug = slugify_unique(instance.title, Subsection)
	elif isinstance(instance, SAQ):
		slug = slugify_unique('saq', SAQ)
	elif isinstance(instance, Numerical):
		slug = slugify_unique('numerical', Numerical)
	elif isinstance(instance, SubsectionImage):
		slug = slugify_unique(instance.caption, SubsectionImage)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Subject)
pre_save.connect(pre_save_post_receiver, sender=Chapter)
pre_save.connect(pre_save_post_receiver, sender=Subtopic)
pre_save.connect(pre_save_post_receiver, sender=Subsection)
pre_save.connect(pre_save_post_receiver, sender=SAQ)
pre_save.connect(pre_save_post_receiver, sender=Numerical)
pre_save.connect(pre_save_post_receiver, sender=SubsectionImage)
