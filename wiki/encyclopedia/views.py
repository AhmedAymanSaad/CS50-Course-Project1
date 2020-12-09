from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from random import seed
from random import randint

class newpageform(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class editpageform(forms.Form):
    content = forms.CharField(widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    return render(request, "encyclopedia/wiki.html",{"name":name , "entry":util.get_entry(name)})

def search(request):
    q = request.GET.get('q')
    entries = util.list_entries()
    list = []
    for entry in entries:
        if q == entry:
            return HttpResponseRedirect("wiki/"+q)
        elif q in entry:
            list.append(entry)
    return render(request, "encyclopedia/search.html", {"list":list})

def newpage(request):
    success = True
    if request.method == "POST":
        form = newpageform(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in entries:
                if title == entry:
                    return render(request, "encyclopedia/newpage.html",{"success":False})
            util.save_entry(title,content)
            return HttpResponseRedirect("wiki/"+title)
        else:
            return render(request, "encyclopedia/newpage.html",{"form":form , "success":success})
    return render(request, "encyclopedia/newpage.html",{"form":newpageform() , "success":success})

def editpage(request,name):
    f = util.get_entry(name)
    default_data = {'content':f}
    if request.method == "POST":
        form = editpageform(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name,content)
            return HttpResponseRedirect("/wiki/"+name)
        else:
            return render(request, "encyclopedia/editpage.html", {"form":form})
    return render(request, "encyclopedia/editpage.html", {"form":editpageform(default_data,auto_id=False),"name":name})

def randompage(request):
    seed()
    entries = util.list_entries()
    range = len(entries)
    value = randint(0, range-1)
    return render(request, "encyclopedia/wiki.html",{"name":entries[value] , "entry":util.get_entry(entries[value])})