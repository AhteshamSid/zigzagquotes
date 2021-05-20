from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import ProfileEditForm, UserEditForm
from django.contrib.auth.views import PasswordChangeView
from django.apps import apps


def EditProfile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data = profile_form.cleaned_data
            new_item = user_form.save(commit=False)
            new_item.author = request.user
            new_item.save()
            new_item = profile_form.save(commit=False)
            new_item.user = request.user
            user_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(new_item.get_absolute_url())
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


# class EditProfile(generic.UpdateView):
#     form_class = EditProfileForm
#     # child_model = apps.get_model('quotes', 'Profile')
#     # child_fields = ('bio', 'date_of_birth', 'profile_pic', 'facebook_url', 'youtube_url', 'twitter_url', 'linkedin_url', 'instagram_url')
#     template_name = 'registration/edit_profile.html'
#     success_url = reverse_lazy('quotes:home')
#
#     def get_object(self, queryset=None):
#         return self.request.user


class ProfilePage(generic.DetailView):
    model = apps.get_model('quotes', 'Profile')
    template_name = "registration/profile_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Profile = apps.get_model('quotes', 'Profile')
        Quote = apps.get_model('quotes', 'Quote')
        query1 = Profile.objects.get(id=self.kwargs['pk'])
        context['post'] = Quote.objects.filter(author=query1.user)
        context['post_len'] = len(Quote.objects.filter(author=query1.user))
        context['query'] = query1
        return context


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('quotes:home')

    def get_object(self):
        return self.request.user


class UserRegister(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('quotes:home')

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
        login(self.request, user)
        return redirect(self.success_url)


class UserDelete(generic.DeleteView):
    model = User
    template_name = "registration/user_delete.html"
    success_url = reverse_lazy('quotes:home')
