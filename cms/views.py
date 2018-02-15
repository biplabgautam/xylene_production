from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
# Create your views here.
from .models import Subject, Chapter, SAQ, Numerical, Subtopic, Subsection, SubsectionImage
from .forms import SubjectForm, ChapterForm, SubtopicForm, SAQForm, NumericalForm, SubsectionForm, SubsectionImageForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def subject_list(request):
	subject_set = Subject.objects.all()
	context = {
		"subjects":subject_set,
	}
	return render(request, "cms/subject_list.html", context)

@login_required
def subject_select(request, sub_pk):
	instance = get_object_or_404(Subject, pk=sub_pk)
	chapter_set = Chapter.objects.filter(subject = instance)
	context = {
		"subject_instance":instance,
		"chapters":chapter_set,
	}
	return render(request, "cms/chapter_list.html", context)

@login_required
def chapter_select(request, chap_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_set = Subtopic.objects.filter(chapter = instance)
	subsection_set = []
	for obj in subtopic_set:
		subsection_set += Subsection.objects.filter(subtopic = obj)

	saq_set = SAQ.objects.filter(chapter = instance)
	numerical_set = Numerical.objects.filter(chapter = instance)
	context = {
		"chapter_instance":instance,
		"subtopics":subtopic_set,
		"subsections":subsection_set,
		"saqs":saq_set,
		"numericals": numerical_set,
	}
	return render(request,"cms/chapter_page.html", context)

@login_required
def saq_list(request, chap_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_set = Subtopic.objects.filter(chapter = instance)
	saq_boolean = True
	saq_set = SAQ.objects.filter(chapter = instance)
	numerical_set = Numerical.objects.filter(chapter = instance)
	context = {
		"subtopics":subtopic_set,
		"chapter_instance":instance,
		"saqs":saq_set,
		"numericals":numerical_set,
		"saq_boolean":saq_boolean,
	}
	return render(request, "cms/saq_list.html", context)

@login_required
def numerical_list(request, chap_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_set = Subtopic.objects.filter(chapter = instance)
	numerical_set = Numerical.objects.filter(chapter = instance)
	saq_set = SAQ.objects.filter(chapter = instance)
	numerical_boolean = True
	context = {
		"subtopics":subtopic_set,
		"chapter_instance":instance,
		"numericals":numerical_set,
		"saqs":saq_set,
		"numerical_boolean":numerical_boolean,
	}
	return render(request, "cms/numerical_list.html", context)

@login_required
def subtopic_select(request, chap_slug, subt_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_set = Subtopic.objects.filter(chapter = instance)
	subtopic_instance = get_object_or_404(Subtopic, slug=subt_slug)
	subsection_set = Subsection.objects.filter(subtopic = subtopic_instance)
	subsection_images_set = SubsectionImage.objects.filter(subtopic = subtopic_instance)

	saq_set = SAQ.objects.filter(chapter = instance)
	numerical_set = Numerical.objects.filter(chapter = instance)

	context = {
		"chapter_instance":instance,
		"subtopics":subtopic_set,
		"subtopic":subtopic_instance,
		"subsections":subsection_set,
		"subsection_images":subsection_images_set,
		"numericals":numerical_set,
		"saqs":saq_set,
	}
	return render(request, "cms/subtopic_detail.html", context)

@login_required
def saq_select(request, chap_slug, saq_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	saq_instance = get_object_or_404(SAQ, slug=saq_slug)
	context = {
		"chapter_instance":instance,
		"saq":saq_instance,
	}
	return render(request, "cms/saq_detail.html", context)

@login_required
def numerical_select(request, chap_slug, num_slug):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	numerical_instance = get_object_or_404(Numerical, slug=num_slug)
	context = {
		"chapter_instance":instance,
		"numerical":numerical_instance,
	}
	return render(request, "cms/numerical_detail.html", context)

#Methods for forms. Creating and editing the content
@login_required
@permission_required('cms.add_subject')
def subject_create(request):
	form = SubjectForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(reverse("cms:subject_list"))

	context = {
		"form":form,
	}
	return render(request, 'cms/subject_form.html', context)

@login_required
@permission_required('cms.change_subject')
def subject_edit(request, sub_pk=None):
	instance = get_object_or_404(Subject, id=sub_pk)
	form = SubjectForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False) 
		instance.save()
		return HttpResponseRedirect(instance.get_subject_select_url())

	context = {
		"instance": instance,
		"form": form,
	}
	return render(request, 'cms/subject_form.html', context)

@login_required
@permission_required('cms.add_chapter')
def chapter_create(request, sub_slug=None):
	subject_instance = get_object_or_404(Subject, slug=sub_slug)
	count = Chapter.objects.filter(subject = subject_instance).count()
	data = {'subject':subject_instance, 'chapter_serial':count+1}
	form = ChapterForm(request.POST or None, request.FILES or None, initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.subject.get_subject_select_url())

	context = {
		"form":form,
		"subject_instance":subject_instance
	}
	return render(request, 'cms/chapter_form.html', context)

@login_required
@permission_required('cms.change_chapter')
def chapter_edit(request, chap_slug=None):
	instance = get_object_or_404(Chapter, slug=chap_slug)
	form = ChapterForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_chapter_select_url())

	context = {
		"form":form, 
		"instance":instance,
	}
	return render(request, 'cms/chapter_form.html', context)

@login_required
@permission_required('cms.add_subtopic')
def subtopic_create(request, chap_slug=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	count = Subtopic.objects.filter(chapter = chapter_instance).count()
	data = {'chapter':chapter_instance, 'subtopic_serial':count+1}
	form = SubtopicForm(chapter_instance.subject, request.POST or None, request.FILES or None, initial = data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_chapter_select_url())

	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/subtopic_form.html', context)

@login_required
@permission_required('cms.change_subtopic')
def subtopic_edit(request, chap_slug=None, subt_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	instance = get_object_or_404(Subtopic, id=subt_pk)
	form = SubtopicForm(chapter_instance.subject, request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_subtopic_select_url())

	context = {
		"form":form,
		"subtopic":instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/subtopic_form.html', context)

@login_required
@permission_required('cms.add_subsection')
def subsection_create(request, chap_slug=None, subt_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	count = Subsection.objects.filter(subtopic = subtopic_instance).count()
	data = {'subtopic':subtopic_instance, 'subsection_serial':count+1}
	form = SubsectionForm(chapter_instance, request.POST or None, initial=data)
	form.chapter = chapter_instance
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/subsection_form.html', context)

@login_required
@permission_required('cms.change_subsection')
def subsection_edit(request,chap_slug=None, subt_pk=None, subsec_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	instance = get_object_or_404(Subsection, id=subsec_pk)
	form = SubsectionForm(chapter_instance, request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"instance":instance,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}

	return render(request, 'cms/subsection_form.html', context)

@login_required
@permission_required('cms.add_subsectionimage')
def subsectionimage_create(request, chap_slug=None, subt_pk=None ):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	count = SubsectionImage.objects.filter(subtopic = subtopic_instance).count()
	data = {'image_serial':count+1}
	form = SubsectionImageForm(subtopic_instance, request.POST or None, request.FILES or None,  initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.subtopic = subtopic_instance
		instance.save()
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/subsection_image_form.html', context)

@login_required
@permission_required('cms.change_subsectionimage')
def subsectionimage_edit(request,chap_slug=None, subt_pk=None, subsecimg_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	instance = get_object_or_404(SubsectionImage, id=subsecimg_pk)
	form = Subsection_imageForm(subtopic_instance, request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"instance":instance,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}

	return render(request, 'cms/subsection_image_form.html', context)

@login_required
@permission_required('cms.add_saq')
def saq_create(request, chap_slug=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	count = SAQ.objects.filter(chapter = chapter_instance).count()
	data = {'chapter':chapter_instance, 'question_serial': count+1}
	form = SAQForm(chapter_instance, request.POST or None, initial = data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.chapter = chapter_instance
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_saq_list_url())
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/saq_form.html', context)

@login_required
@permission_required('cms.change_saq')
def saq_edit(request, chap_slug=None, saq_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	instance = get_object_or_404(SAQ, id=saq_pk)
	form = SAQForm(chapter_instance, request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_saq_list_url())

	context = {
		"form":form, 
		"instance":instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/saq_form.html', context)

@login_required
@permission_required('cms.add_numerical')
def numerical_create(request, chap_slug=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	count = Numerical.objects.filter(chapter = chapter_instance).count()
	data = {'chapter':chapter_instance, 'numerical_serial': count+1}
	form = NumericalForm(chapter_instance, request.POST or None, initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.chapter = chapter_instance
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_numerical_list_url())
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/numerical_form.html', context)

@login_required
@permission_required('cms.change_numerical')
def numerical_edit(request,chap_slug=None, num_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	instance = get_object_or_404(Numerical, id=num_pk)
	form = NumericalForm(chapter_instance, request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(chapter_instance.get_numerical_list_url())

	context = {
		"form":form,
		"instance":instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'cms/numerical_form.html', context)

