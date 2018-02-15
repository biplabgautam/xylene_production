from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import TempSubsectionForm, TempSAQForm, TempNumericalForm, TempSubsectionImageForm
from cms.models import Subject, Chapter, Subtopic, Subsection, Numerical, SAQ, SubsectionImage
from .models import TempSubsection, TempSAQ, TempNumerical, TempSubsectionImage

User = get_user_model()
# Create your views here.
#These view functions are called when member users create contents (subsections, saqs, numericals, images)
#These contents are stored in temporary models (databases) until approved.

@login_required
@permission_required('tempcms.add_tempsubsection')
def tempsubsection_create(request, chap_slug=None, subt_pk=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	count = Subsection.objects.filter(subtopic = subtopic_instance).count()
	#Pending count counts the pending created items in the temporary database.
	#This is useful for automatic serial numbering for form fill up.
	pending_count = TempSubsection.objects.filter(subtopic = subtopic_instance).filter(edited_bool = False).count()

	data = {
	'subtopic':subtopic_instance,
	'subsection_serial':count+pending_count+1,
	}
	form = TempSubsectionForm(chapter_instance, request.POST or None, initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.last_modified_by = request.user
		instance.save()
		messages.success(request, 'Your content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/subsection_form.html', context)

@login_required
@permission_required('tempcms.change_tempsubsection')
def tempsubsection_edit(request,chap_slug=None, subt_pk=None, subsec_pk=None):
	#First we check whether the user has some pending edits on the same subsection or not
	#If yes then allow him to edit the pending subsection.
	user_instance = request.user
	pending_subsection_set = TempSubsection.objects.filter(last_modified_by = user_instance)
	pending_subsection_bool = pending_subsection_set.filter(temp_id = subsec_pk).exists()
	if (pending_subsection_bool):
		pending_subsection_item = pending_subsection_set.get(temp_id = subsec_pk)
		subtopic_instance = pending_subsection_item.subtopic
		chapter_instance = subtopic_instance.chapter
		form = TempSubsectionForm(chapter_instance, request.POST or None, instance = pending_subsection_item)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
			return HttpResponseRedirect(reverse('accounts:pending_content'))

		context = {
		"form":form,
		"subtopic_instance": subtopic_instance,
		"chapter_instance": chapter_instance,
		}
		return render(request, 'tempcms/subsection_form.html', context)
	#If no, then create a new tempsubsection
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	instance = get_object_or_404(Subsection, id=subsec_pk)
	data = {
	'subsection_serial':instance.subsection_serial,
	'title':instance.title,
	'subtopic':instance.subtopic,
	'content':instance.content,
	'remarks':instance.remarks,
	}

	form = TempSubsectionForm(chapter_instance, request.POST or None, initial = data)
	if form.is_valid():
		temp_instance = form.save(commit=False)
		temp_instance.edited_bool = True
		temp_instance.temp_id = subsec_pk
		temp_instance.last_modified_by = request.user
		temp_instance.save()
		messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"instance":instance,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}

	return render(request, 'tempcms/subsection_form.html', context)

@login_required
@permission_required('tempcms.add_tempsaq')
def tempsaq_create(request, chap_slug=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	count = SAQ.objects.filter(chapter = chapter_instance).count()
	pending_count = TempSAQ.objects.filter(chapter = chapter_instance).filter(edited_bool = False).count()
	data = {
	'chapter':chapter_instance,
	'question_serial': count+pending_count+1,
	}
	form = TempSAQForm(chapter_instance, request.POST or None, request.FILES or None, initial = data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.chapter = chapter_instance
		instance.last_modified_by = request.user
		instance.save()
		messages.success(request, 'Your content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(chapter_instance.get_saq_list_url())
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/saq_form.html', context)

@login_required
@permission_required('tempcms.change_tempsaq')
def tempsaq_edit(request, chap_slug=None, saq_pk=None):
	#Checking if tempsaq exists for same question edited by same user or not
	user_instance = request.user
	pending_saq_set = TempSAQ.objects.filter(last_modified_by = user_instance)
	pending_saq_bool = pending_saq_set.filter(temp_id = saq_pk).exists()
	if (pending_saq_bool):
		tempsaq_instance = pending_saq_set.get(temp_id = saq_pk)
		chapter_instance = tempsaq_instance.chapter
		form = TempSAQForm(chapter_instance, request.POST or None, request.FILES or None, instance = tempsaq_instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
			return HttpResponseRedirect(reverse('accounts:pending_content'))

		context = {
		"form":form,
		"chapter_instance": chapter_instance,
		}
		return render(request, 'tempcms/saq_form.html', context)
	#If that user has edited the content which is not in his pending state then,
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	instance = get_object_or_404(SAQ, id=saq_pk)
	data = {
	'question_serial':instance.question_serial,
	'question':instance.question,
	'answer':instance.answer,
	'important':instance.important,
	'remarks':instance.remarks,
	'subtopic':instance.subtopic,
	'display_image':instance.display_image,

	}
	form = TempSAQForm(chapter_instance, request.POST or None, initial=data)
	if form.is_valid():
		temp_instance = form.save(commit=False)
		temp_instance.chapter = chapter_instance
		temp_instance.edited_bool = True
		temp_instance.temp_id = saq_pk
		temp_instance.last_modified_by = request.user
		temp_instance.save()
		return HttpResponseRedirect(chapter_instance.get_saq_list_url())

	context = {
		"form":form,
		"instance":instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/saq_form.html', context)

@login_required
@permission_required('tempcms.add_tempnumerical')
def tempnumerical_create(request, chap_slug=None):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	count = Numerical.objects.filter(chapter = chapter_instance).count()
	pending_count = TempNumerical.objects.filter(chapter = chapter_instance).filter(edited_bool = False).count()
	data = {
	'chapter':chapter_instance,
	'numerical_serial': count+pending_count+1,
	}
	form = TempNumericalForm(chapter_instance, request.POST or None, request.FILES or None, initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.chapter = chapter_instance
		instance.last_modified_by = request.user
		instance.save()
		messages.success(request, 'Your content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(chapter_instance.get_numerical_list_url())
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/numerical_form.html', context)

@login_required
@permission_required('tempcms.change_tempnumerical')
def tempnumerical_edit(request,chap_slug=None, num_pk=None):
	#Checking if tempnumerical exists for same question edited by same user or not
	user_instance = request.user
	pending_numerical_set = TempNumerical.objects.filter(last_modified_by = user_instance)
	pending_numerical_bool = pending_numerical_set.filter(temp_id = num_pk).exists()
	if (pending_numerical_bool):
		tempnumerical_instance = pending_numerical_set.get(temp_id = num_pk)
		chapter_instance = tempnumerical_instance.chapter
		form = TempNumericalForm(chapter_instance, request.POST or None, request.FILES or None, instance = tempnumerical_instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
			return HttpResponseRedirect(reverse('accounts:pending_content'))

		context = {
		"form":form,
		"chapter_instance": chapter_instance,
		}
		return render(request, 'tempcms/numerical_form.html', context)
	#If that user has edited the content which is not in his pending state then,
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	instance = get_object_or_404(Numerical, id=num_pk)
	data = {
			'numerical_serial':instance.numerical_serial,
			'question':instance.question,
			'answer':instance.answer,
			'important':instance.important,
			'remarks':instance.remarks,
			'subtopic':instance.subtopic,
			'display_image':instance.display_image,
	}
	form = TempNumericalForm(chapter_instance, request.POST or None, request.FILES or None, initial = data)
	if form.is_valid():
		temp_instance = form.save(commit=False)
		temp_instance.chapter = chapter_instance
		temp_instance.edited_bool = True
		temp_instance.temp_id = num_pk
		temp_instance.last_modified_by = request.user
		temp_instance.save()
		messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(chapter_instance.get_numerical_list_url())

	context = {
		"form":form,
		"instance":instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/numerical_form.html', context)

@login_required
@permission_required('tempcms.add_tempsubsectionimage')
def tempsubsectionimage_create(request, chap_slug=None, subt_pk=None ):
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	count = SubsectionImage.objects.filter(subtopic = subtopic_instance).count()
	pending_count = TempSubsectionImage.objects.filter(subtopic = subtopic_instance).filter(edited_bool = False).count()
	data = {
	'image_serial':count+1,
	}
	form = TempSubsectionImageForm(subtopic_instance, request.POST or None, request.FILES or None,  initial=data)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.subtopic = subtopic_instance
		instance.last_modified_by = request.user
		instance.save()
		messages.success(request, 'Your content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(subtopic_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'tempcms/subsection_image_form.html', context)

@login_required
@permission_required('tempcms.change_tempsubsectionimage')
def tempsubsectionimage_edit(request,chap_slug=None, subt_pk=None, subsecimg_pk=None):
	#First we check whether the user has some pending edits on the same image or not
	#If yes then allow him to edit the pending subsection.
	user_instance = request.user
	pending_image_set = TempSubsectionImage.objects.filter(last_modified_by = user_instance)
	pending_image_bool = pending_image_set.filter(temp_id = subsecimg_pk).exists()
	if (pending_image_bool):
		pending_subsection_image_instance = pending_image_set.get(temp_id = subsecimg_pk)
		subtopic_instance = pending_subsection_image_instance.subtopic
		chapter_instance = subtopic_instance.chapter
		form = TempSubsectionImageForm(chapter_instance, request.POST or None, instance = pending_subsection_image_instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
			return HttpResponseRedirect(reverse('accounts:pending_content'))

		context = {
		"form":form,
		"subtopic_instance": subtopic_instance,
		"chapter_instance": chapter_instance,
		}
		return render(request, 'tempcms/subsection_image_form.html', context)
	#If no, then create a new tempsubsection image
	chapter_instance = get_object_or_404(Chapter, slug=chap_slug)
	subtopic_instance = get_object_or_404(Subtopic, id=subt_pk)
	instance = get_object_or_404(SubsectionImage, id=subsecimg_pk)
	data = {
			'image_serial':instance.image_serial,
			'image':instance.image,
			'caption':instance.caption,
			'subsection':instance.subsection,
	}
	form = TempSubsectionImageForm(subtopic_instance, request.POST or None, request.FILES or None, initial = data)
	if form.is_valid():
		temp_instance = form.save(commit=False)
		temp_instance.edited_bool = True
		temp_instance.temp_id = subsecimg_pk
		temp_instance.last_modified_by = request.user
		temp_instance.save()
		messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
		return HttpResponseRedirect(chapter_instance.get_subtopic_select_url())

	context = {
		"form":form,
		"instance":instance,
		"subtopic_instance":subtopic_instance,
		"chapter_instance":chapter_instance,
	}

	return render(request, 'tempcms/subsection_image_form.html', context)

#These view functions are used to view the pending contents submitted by the member users.

@login_required
@permission_required('tempcms.view_pending_subsections')
def pending_subsections (request):
	subsection_set = TempSubsection.objects.all()
	context = {
		"subsection_set":subsection_set,
	}
	return render(request, 'pending/subsections.html', context)

@login_required
@permission_required('tempcms.view_pending_saqs')
def pending_saqs (request):
	saq_set = TempSAQ.objects.all()
	saq_boolean = True
	context = {
		"saq_set":saq_set,
		"saq_boolean": saq_boolean,
	}
	return render(request, 'pending/saqs.html', context)

@login_required
@permission_required('tempcms.view_pending_numericals')
def pending_numericals (request):
	numerical_set = TempNumerical.objects.all()
	numerical_boolean = True
	context = {
		"numerical_set":numerical_set,
		"numerical_boolean": numerical_boolean,
	}
	return render(request, 'pending/numericals.html', context)

@login_required
@permission_required('tempcms.view_pending_subsection_images')
def pending_subsection_images (request):
	subsection_images_set = TempSubsectionImage.objects.all()
	subsection_image_boolean = True
	context = {
		"subsection_images_set":subsection_images_set,
		"subsection_image_boolean":subsection_image_boolean,
	}
	return render(request, 'pending/subsection_images.html', context)

#View functions to approve the pending contents

@login_required
@permission_required('tempcms.approve_pending_subsections')
def approve_subsection(request, tempsubsec_pk = None):
	tempsubsection_instance = get_object_or_404(TempSubsection, id = tempsubsec_pk)
	subtopic_instance = tempsubsection_instance.subtopic
	chapter_instance = subtopic_instance.chapter
	form = TempSubsectionForm(chapter_instance, request.POST or None, instance = tempsubsection_instance)
	if form.is_valid():
		if 'save' in request.POST:
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'The content has been saved. It has not been published.')
			return HttpResponseRedirect(reverse('tcms:pending_subsections'))
		elif 'approve' in request.POST:
			if (not tempsubsection_instance.edited_bool):
				#This means the content is created
				instance = form.save(commit=False)
				instance.save()
				actual_instance = Subsection(
						subsection_serial = instance.subsection_serial,
						title = instance.title,
						content = instance.content,
						subtopic = instance.subtopic,
						remarks = instance.remarks,
						date_modified = instance.date_modified,
						created_by = instance.last_modified_by,
						last_modified_by = instance.last_modified_by,
						approved_by = request.user,
					)
				actual_instance.save()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				tempsubsection_instance.delete()
				return HttpResponseRedirect(reverse('tcms:pending_subsections'))
			else:
				#This means the content was edited
				instance = form.save(commit=False)
				instance.save()

				actual_instance = Subsection.objects.get(pk = instance.temp_id)
				actual_instance.subsection_serial = instance.subsection_serial
				actual_instance.title = instance.title
				actual_instance.content = instance.content
				actual_instance.subtopic = instance.subtopic
				actual_instance.remarks = instance.remarks
				actual_instance.date_modified = instance.date_modified
				actual_instance.last_modified_by = instance.last_modified_by
				actual_instance.approved_by = request.user

				actual_instance.save(update_fields=['subsection_serial', 'title', 'content', 'subtopic', 'remarks', 'date_modified', 'last_modified_by', 'approved_by'])
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')

				tempsubsection_instance.delete()
				return HttpResponseRedirect(reverse('tcms:pending_subsections'))
		elif 'delete' in request.POST:
			tempsubsection_instance.delete()
			messages.warning(request, 'The content has been deleted successfully.')
			return HttpResponseRedirect(reverse('tcms:pending_subsections'))
	context = {
		"form":form,
		"subtopic_instance": subtopic_instance,
		"chapter_instance": chapter_instance,
	}
	return render(request, 'pending/subsection_approval_form.html', context)

@login_required
@permission_required('tempcms.approve_pending_numericals')
def approve_numerical(request, tempnum_pk):
	tempnumerical_instance = get_object_or_404(TempNumerical, id=tempnum_pk)
	chapter_instance = tempnumerical_instance.chapter
	form = TempNumericalForm(chapter_instance, request.POST or None, instance = tempnumerical_instance)
	if form.is_valid():
		if 'save' in request.POST:
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'The content has been saved successfully. It has not been published.')
			return HttpResponseRedirect(reverse('tcms:pending_numericals'))
		elif 'approve' in request.POST:
			if (not tempnumerical_instance.edited_bool):
				#This means the numerical content was created
				#The content may be edited in that approval form as well.
				instance = form.save(commit=False)
				instance.save()
				actual_instance = Numerical(
						numerical_serial = instance.numerical_serial,
						question = instance.question,
						answer = instance.answer,
						important = instance.important,
						remarks = instance.remarks,
						chapter = instance.chapter,
						subtopic = instance.subtopic,
						display_image = instance.display_image,
						height_field = instance.height_field,
						width_field = instance.width_field,
						date_modified = instance.date_modified,

						created_by = instance.last_modified_by,
						last_modified_by = instance.last_modified_by,
						approved_by = request.user,
					)
				actual_instance.save()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				tempnumerical_instance.delete()
				messages.warning(request, 'The content has been deleted successfully.')
				return HttpResponseRedirect(reverse('tcms:pending_numericals'))
			else:
				#this means the content was edited
				instance = form.save(commit=False)
				instance.save()

				actual_instance = Numerical.objects.get(pk = instance.temp_id)
				actual_instance.numerical_serial = instance.numerical_serial
				actual_instance.question = instance.question
				actual_instance.answer = instance.answer
				actual_instance.important = instance.important
				actual_instance.remarks = instance.remarks
				actual_instance.chapter = instance.chapter
				actual_instance.subtopic = instance.subtopic
				actual_instance.display_image = instance.display_image
				actual_instance.height_field = instance.height_field
				actual_instance.width_field = instance.width_field
				actual_instance.date_modified = instance.date_modified

				actual_instance.last_modified_by = instance.last_modified_by
				actual_instance.approved_by = request.user

				actual_instance.save(update_fields=['numerical_serial','question', 'answer', 'important', 'remarks', 'chapter', 'subtopic', 'display_image', 'height_field', 'width_field', 'date_modified', 'last_modified_by', 'approved_by'])
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				tempnumerical_instance.delete()
				return HttpResponseRedirect(reverse('tcms:pending_numericals'))
		elif 'delete' in request.POST:
			tempnumerical_instance.delete()
			return HttpResponseRedirect(reverse('tcms:pending_numericals'))
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'pending/numerical_approval_form.html', context)

@login_required
@permission_required('tempcms.approve_pending_saqs')
def approve_saq(request, tempsaq_pk):
	tempsaq_instance = get_object_or_404(TempSAQ, id = tempsaq_pk)
	chapter_instance = tempsaq_instance.chapter
	form = TempSAQForm(chapter_instance, request.POST or None, instance = tempsaq_instance)
	if form.is_valid():
		if 'save' in request.POST:
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'The content has been saved successfully. It has not been published.')
			return HttpResponseRedirect(reverse('tcms:pending_saqs'))
		elif 'approve' in request.POST:
			if (not tempsaq_instance.edited_bool):
				#This means the numerical content was created
				#The content may be edited in that form as well.
				instance = form.save(commit=False)
				instance.save()
				actual_instance = SAQ(
						question_serial = instance.question_serial,
						question = instance.question,
						answer = instance.answer,
						important = instance.important,
						remarks = instance.remarks,
						chapter = instance.chapter,
						subtopic = instance.subtopic,
						display_image = instance.display_image,
						height_field = instance.height_field,
						width_field = instance.width_field,
						date_modified = instance.date_modified,

						created_by = instance.last_modified_by,
						last_modified_by = instance.last_modified_by,
						approved_by = request.user,
					)
				actual_instance.save()
				tempsaq_instance.delete()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				return HttpResponseRedirect(reverse('tcms:pending_saqs'))
			else:
				#this means the content was edited
				instance = form.save(commit=False)
				instance.save()

				actual_instance = SAQ.objects.get(pk = instance.temp_id)
				actual_instance.question_serial = instance.question_serial
				actual_instance.question = instance.question
				actual_instance.answer = instance.answer
				actual_instance.important = instance.important
				actual_instance.remarks = instance.remarks
				actual_instance.chapter = instance.chapter
				actual_instance.subtopic = instance.subtopic
				actual_instance.display_image = instance.display_image
				actual_instance.height_field = instance.height_field
				actual_instance.width_field = instance.width_field
				actual_instance.date_modified = instance.date_modified

				actual_instance.last_modified_by = instance.last_modified_by
				actual_instance.approved_by = request.user

				actual_instance.save(update_fields=['question_serial','question', 'answer', 'important', 'remarks', 'chapter', 'subtopic', 'display_image', 'height_field', 'width_field', 'date_modified', 'last_modified_by', 'approved_by'])
				tempsaq_instance.delete()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				return HttpResponseRedirect(reverse('tcms:pending_saqs'))
		elif 'delete' in request.POST:
			tempsaq_instance.delete()
			messages.warning(request, 'The content has been deleted successfully.')
			return HttpResponseRedirect(reverse('tcms:pending_saqs'))
	context = {
		"form":form,
		"chapter_instance":chapter_instance,
	}
	return render(request, 'pending/saq_approval_form.html', context)

@login_required
@permission_required('tempcms.approve_pending_subsection_images')
def approve_subsection_image(request, tempsubsecimg_pk = None):
	tempsubsection_image_instance = get_object_or_404(TempSubsectionImage, id = tempsubsecimg_pk)
	subsection_instance = tempsubsection_image_instance.subsection
	subtopic_instance = tempsubsection_image_instance.subtopic
	chapter_instance = subtopic_instance.chapter
	form = TempSubsectionImageForm(subtopic_instance, request.POST or None, instance = tempsubsection_image_instance)
	if form.is_valid():
		if 'save' in request.POST:
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'The content has been saved successfully. It has not been published.')
			return HttpResponseRedirect(reverse('tcms:pending_subsection_images'))
		elif 'approve' in request.POST:
			if (not tempsubsection_image_instance.edited_bool):
				#This means the content is created
				instance = form.save(commit=False)
				instance.save()

				actual_instance = SubsectionImage(
							image_serial = instance.image_serial,
							caption = instance.caption,
							image = instance.image,
							height_field = instance.height_field,
							width_field = instance.width_field,
							subsection = instance.subsection,
							subtopic = instance.subtopic,
							date_modified = instance.date_modified,

							created_by = instance.last_modified_by,
							last_modified_by = instance.last_modified_by,
							approved_by = request.user,
					)
				actual_instance.save()
				tempsubsection_image_instance.delete()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				return HttpResponseRedirect(reverse('tcms:pending_subsection_images'))
			else:
				#This means the content was edited
				instance = form.save(commit=False)
				instance.save()

				actual_instance = SubsectionImage.objects.get(pk = instance.temp_id)
				actual_instance.image_serial = instance.image_serial
				actual_instance.caption = instance.caption
				actual_instance.image = instance.image
				actual_instance.height_field = instance.height_field
				actual_instance.width_field = instance.width_field
				actual_instance.subsection = instance.subsection
				actual_instance.subtopic = instance.subtopic
				actual_instance.date_modified = instance.date_modified

				actual_instance.last_modified_by = instance.last_modified_by
				actual_instance.approved_by = request.user

				actual_instance.save(update_fields=['image_serial','caption','image','height_field','width_field','subsection', 'subtopic', 'date_modified', 'last_modified_by', 'approved_by'])
				tempsubsection_image_instance.delete()
				messages.success(request, 'The content has been approved successfully. It has been published to the main database.')
				return HttpResponseRedirect(reverse('tcms:pending_subsection_images'))
		elif 'delete' in request.POST:
			tempsubsection_image_instance.delete()
			messages.warning(request, 'The content has been deleted successfully.')
			return HttpResponseRedirect(reverse('tcms:pending_subsection_images'))
	context = {
		"form":form,
		"subtopic_instance": subtopic_instance,
		"chapter_instance": chapter_instance,
	}
	return render(request, 'pending/subsection_image_approval_form.html', context)
