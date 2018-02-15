from django import forms
from .models import Subject, Chapter, Subtopic, SAQ, Numerical, Subsection, SubsectionImage

from pagedown.widgets import PagedownWidget

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = [
			'subject_name',
			'grade',
			'faculty',
			'poster_image',
		]

class ChapterForm(forms.ModelForm):
	class Meta:
		model = Chapter
		fields = [
			'chapter_serial',
			'chapter_name',
			'section',
			'subject',
			'poster_image',
		]

class SubtopicForm(forms.ModelForm):
	class Meta:
		model = Subtopic
		fields = [
			'subtopic_serial',
			'title',
			'chapter',
			'remarks',
			'poster_image',
		]

	def __init__(self, subject, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['chapter'].queryset = \
		self.fields['chapter'].queryset.filter(subject=subject)

class SubsectionForm(forms.ModelForm):
	content = forms.CharField(widget = PagedownWidget)
	class Meta:
		model = Subsection
		fields = [
			'subsection_serial',
			'title',
			'subtopic',
			'content',
			'remarks',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class SAQForm(forms.ModelForm):
	question = forms.CharField(widget=PagedownWidget)
	answer = forms.CharField(widget=PagedownWidget)

	class Meta:
		model = SAQ
		fields = [
			'question_serial',
			'question',
			'answer',
			'important',
			'remarks',
			'subtopic',
			'display_image',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class NumericalForm(forms.ModelForm):
	question = forms.CharField(widget=PagedownWidget)
	answer = forms.CharField(widget=PagedownWidget)
	class Meta:
		model = Numerical
		fields = [
			'numerical_serial',
			'question',
			'answer',
			'important',
			'remarks',
			'subtopic',
			'display_image',
		]

	def __init__(self, chapter, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subtopic'].queryset = \
		self.fields['subtopic'].queryset.filter(chapter=chapter)

class SubsectionImageForm(forms.ModelForm):
	class Meta:
		model = SubsectionImage
		fields = [
			'image_serial',
			'image',
			'caption',
			'subsection',
	]
	def __init__(self, subtopic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subsection'].queryset = \
		self.fields['subsection'].queryset.filter(subtopic=subtopic)
