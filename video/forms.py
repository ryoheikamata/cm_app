from django import forms
from django.contrib.auth.models import User
from .models import Video, Category
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class Video_post(forms.Form):
    category_data = Category.objects.all().values_list('name', 'name')
    category_choice = []
    for category in category_data:
        category_choice.append(category)

    # author = forms.ChoiceField(label='user', widget=forms.Select, choices=list(author_choice.items()))
    caption = forms.CharField(max_length=100, label='タイトル & タレント名..')
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=category_choice)
    video = forms.FileField(required=False)
    # thmub = forms.FileField()
    content = forms.CharField(label='content', widget=forms.Textarea(attrs={'placeholder': "クライアント名、タレント名、代理店、OA開始日、、、などなど"}))

    # class Meta:
    #     model = Video
    #     video = ('video', 'readonly')

    # class Meta:
    #     model = Video
    #     fields = ('author', 'caption', 'category', 'video', 'content')
    #

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # widgets ={
        #     'author': forms.Select(attrs={'class': 'form-control'}),
        #     'caption': forms.TextInput(attrs={'class': 'form_control'}),
        #     'category': forms.Select(choices=choice_list, attrs={'class': 'form_control'}),
        #     'video': forms.FileField(attrs={'class': 'form_control'}),
        #     'content': forms.TextInput(attrs={'class': 'form_control'})
        # }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
