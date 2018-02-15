from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import(
	authenticate, 
	get_user_model,
	login,
	logout,
	update_session_auth_hash,
	)
from .forms import UserLoginForm, ChangeCredentialsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from tempcms.models import TempSubsection, TempSAQ, TempNumerical, TempSubsectionImage
from tempcms.forms import TempSubsectionForm, TempSAQForm, TempNumericalForm, TempSubsectionImageForm
# Create your views here.

User = get_user_model()

def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password=password)
		login(request, user)
		return redirect("cms:subject_list")

	return render(request, "login_form.html", {"form":form, "title":title})

def logout_view(request):
	logout(request)
	messages.success(request, 'You have logged out.')
	return redirect("login")

@login_required
def change_credentials_view(request):
	title = "Change Credentials"
	if request.user.is_authenticated():
		user_instance = request.user
		form = ChangeCredentialsForm(request.POST or None, instance = user_instance)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			messages.success(request, 'You have changed your credentials.')
			return redirect("/")
		context = {
		"form":form,
		"title":title,
			}
		return render(request, "login_form.html", context)
	else:
		raise Http404("Invalid user.")

@login_required
def change_password_view(request):
    title = "Change Password"
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect("/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login_form.html', {
        'form': form,
        'title': title,
    })

#View function to see all pending contents of that particular user
@login_required
def pending_content(request):
	if request.user.is_authenticated():
		user_instance = request.user
		pending_subsection_set = TempSubsection.objects.filter(last_modified_by = user_instance)
		pending_saq_set = TempSAQ.objects.filter(last_modified_by = user_instance)
		pending_numerical_set = TempNumerical.objects.filter(last_modified_by = user_instance)
		pending_subsection_image_set = TempSubsectionImage.objects.filter(last_modified_by = user_instance)
		context = {
		"subsections": pending_subsection_set,
		"saqs": pending_saq_set,
		"numericals": pending_numerical_set,
		"subsection_images": pending_subsection_image_set,
		}
		return render(request, 'accounts/user_pending_content.html', context)

	else:
		raise Http404("Invalid User")

#View functions to view details of each pending content
#Subsection, SAQ, Numerical,etc.
@login_required
def see_tempsubsection(request, tempsubsec_pk = None):
	tempsubsection_instance = get_object_or_404(TempSubsection, id=tempsubsec_pk)
	if (request.user == tempsubsection_instance.last_modified_by):
		subtopic_instance = tempsubsection_instance.subtopic
		chapter_instance = subtopic_instance.chapter
		form = TempSubsectionForm(chapter_instance, request.POST or None, instance = tempsubsection_instance)
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
	else:
		raise Http404("Invalid User")

@login_required
def see_tempsaq(request, tempsaq_pk = None):
	tempsaq_instance = get_object_or_404(TempSAQ, id=tempsaq_pk)
	if (request.user == tempsaq_instance.last_modified_by):
		chapter_instance = tempsaq_instance.chapter
		form = TempSAQForm(chapter_instance, request.POST or None, instance = tempsaq_instance)
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
	else:
		raise Http404("Invalid User")

@login_required
def see_tempnumerical(request, tempnum_pk = None):
	tempnumerical_instance = get_object_or_404(TempNumerical, id=tempnum_pk)
	if (request.user == tempnumerical_instance.last_modified_by):
		chapter_instance = tempnumerical_instance.chapter
		form = TempNumericalForm(chapter_instance, request.POST or None, instance = tempnumerical_instance)
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
	else:
		raise Http404("Invalid User")

@login_required
def see_tempsubsection_image(request, tempsubsecimg_pk = None):
	tempsubsection_image_instance = get_object_or_404(TempSubsectionImage, id=tempsubsecimg_pk)
	if (request.user == tempsubsection_image_instance.last_modified_by):
		subsection_instance = tempsubsection_image_instance.subsection
		subtopic_instance = tempsubsection_image_instance.subtopic
		chapter_instance = subtopic_instance.chapter
		form = TempSubsectionImageForm(subtopic_instance, request.POST or None, instance = tempsubsection_image_instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, 'Your edited content is submitted successfully. It will be reviewed before publishing.')
			return HttpResponseRedirect(reverse('accounts:pending_content'))

		context = {
		"form":form,
		"subsection_instance": subsection_instance,
		"subtopic_instance": subtopic_instance,
		"chapter_instance": chapter_instance,
		}
		return render(request, 'tempcms/subsection_image_form.html', context)
	else:
		raise Http404("Invalid User")