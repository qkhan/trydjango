from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, Http404
from django.utils import timezone
from .models import Post
from .forms import TestForm, PostModelForm

# Create your views here.
# def home_old(request):
#     initial_dict = {
#         "some_text": "Text",
#         "boolean": True,
#         "integer": "123"
#     }
#     print ("Hello Qaisar")
#     form = TestForm(request.POST, initial=initial_dict)
#     #print form
#     if request.method == "POST":
#         form = TestForm(request.POST)
#     elif request.method == "GET":
#         form = TestForm(user=request.user
#     # if form.is_valid():
#     #     print(form.cleaned_data)
#     #     print(form.cleaned_data.get("some_text"))
#     #     print(form.cleaned_data.get("email"))
#     #     print(form.cleaned_data.get("email2"))
#
#     return render(request, "test_form.html", {"form": form})

def formset_view(request):
    if request.user.is_authenticated():
        PostModelFormset = modelformset_factory(Post, form=PostModelForm, extra=0)
        formset = PostModelFormset(request.POST or None,
                    queryset=Post.objects.filter(user=request.user))
        if formset.is_valid():
            for form in formset:
                print ("QKHAN: ", form.cleaned_data.get("title"))
                obj = form.save(commit=False)
                if form.cleaned_data:
                    if not form.cleaned_data.get("publish"):
                        obj.publish = timezone.now()
                    obj.save()
        context = {
            "formset": formset
        }
    return render(request, "form_set.html", context)

def home(request):

    form = PostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        print(obj.title)
        obj.title = "Some random title"
        obj.publish = timezone.now()
        form.save()
    if form.has_error:
        #print(form.errors.as_json())
        #print(form.errors.as_text())
        data = form.errors.iteritems()
        for key, value in data:
            #print(dir(value))
            print (key, value)
            error_str = "{field}: {error}". format(
                field=key,
                error=value.as_text()
            )
            print(error_str)
        print(form.non_field_errors())
    return render(request, "manual_form.html", {"form": form})
    #return render(request, "test_form.html", {"form": form})
