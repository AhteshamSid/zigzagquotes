from django import forms

from .models import Quote, Category, Comment

choices = Category.objects.all().values_list('name', 'name')

choice_list = []
for item in choices:
    choice_list.append(item)
for x in Quote.objects.values("category").distinct().values_list('category', 'category'):
    if x not in choices:
        choice_list.append(x)


class AddQuotesForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('title', 'body', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quote Title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your Quote'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class': 'body-form', 'placeholder': 'Enter your Comment'}),
        }
