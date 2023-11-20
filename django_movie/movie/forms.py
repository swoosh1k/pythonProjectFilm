from django import forms
from captcha.fields import CaptchaField
from .models import Reviews, Rating, RatingStar



class ReviewForm(forms.ModelForm):
    '''Формв отзывов'''
    captcha = CaptchaField()
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', 'captcha')



class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset = RatingStar.objects.all(), widget = forms.RadioSelect, empty_label = None)


    class Meta:
        model = Rating
        fields = ("star",)