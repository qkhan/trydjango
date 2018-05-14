from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Post
from django.utils.text import slugify

SOME_CHOICES = [
    ('db-value', 'Display Value'),
    ('db-value2', 'Display Value2'),
    ('db-value3', 'Display Value3'),
]


INTS_CHOICES = [tuple([x,x]) for x in range(0, 102)]

YEARS = [x for x in range(1980, 2031)]

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "slug",
            "image",
            "content"
        ]
        exclude = ["height_field","width_field"]
        labels = {
            "title": "this is the title label",
            "slug": "This is slug",
        }
        help_text = {
            "title": "this is title label",
            "slug": "This is slug",
        }
        error_messages = {
            "title": {
                "max_length": "This title is too long.",
                "required": "This title field is required",
            },
            "slug": {
                "max_length": "This title is too long",
                "required": "This title field is required",
                "unique" :  "The slug field must be unique",
            }
        }

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields["title"].error_messages = {
                "max_length": "This title is too long.",
                "required": "This title field is required",
        }
        self.fields["slug"].error_messages = {
                "max_length": "This title is too long.",
                "required": "This title field is required",
        }

        for field in self.fields.values():
            field.error_messages = {
                'required': "You know, {fieldname} is required".format(fieldname=field.label),
            }

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        print title
        return title

    def save(self, commit=True, *args, **kwargs):
        obj = super(PostModelForm, self).save(commit=False, *args, **kwargs)
        obj.slug = slugify(obj.title)
        obj.publish = "2018-05-04"
        if commit:
            obj.save()
        return obj

class TestForm(forms.Form):
    date_field = forms.DateField(initial="2010-11-20", widget=SelectDateWidget(years=YEARS))
    some_text = forms.CharField(label='Text', widget=forms.Textarea(attrs={"rows": 4, "cols": 10}))
    choices = forms.CharField(label='Text', widget=forms.Select(choices=SOME_CHOICES))
    boolean = forms.BooleanField()
    integer = forms.IntegerField(initial=101, widget=forms.Select(choices=INTS_CHOICES))
    email = forms.EmailField(min_length=10)


    def __init__(self, user=None, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        print("QK", user)
        if user:
            self.fields["some_text"].initial = user.username

    def clean_integer(self, *args, **kwargs):
        integer = self.cleaned_data.get("integer")
        if integer < 10:
            raise forms.ValidationError("The integer must be greater than 10")
        return integer

    def clean_some_text(self, *args, **kwars):
        some_text = self.cleaned_data.get("some_text")
        if len(some_text) < 5:
            raise forms.ValidationError("Ensure the text is greater than 5 characters")
        return some_text
