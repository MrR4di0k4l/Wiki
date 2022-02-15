from django.shortcuts import render as _render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import markdown2
from . import util
import random
from django.conf import settings

def index(request):
    List = util.list_entries()
    if request.method == "POST":
        search = request.POST.get("search")
        letter = request.POST.get("letter")
        if search is not None:
            search = search.lower().strip()
            for entry in List:
                if search == entry.lower():
                    return redirect("wiki", title=entry)

            List = list(filter(lambda x: search in x.lower(), List))
            if not List:
                return redirect(notFound)

        elif letter is not None:
            letter = letter.strip().lower()
            List = list(
                filter(lambda x: x.lower().startswith(letter), List)
            )
    return render(request, "encyclopedia/index.html", {
        "entries": List
    })
    
def wiki(request, title):
    entry_list = util.list_entries()

    title = title.strip()
    wiki = [entry for entry in entry_list 
            if title.lower() in entry.lower()]

    if not wiki or wiki is None:
        return redirect(notFound)

    entry = util.get_entry(wiki[0])

    return render(request, "encyclopedia/entry.html",{
        "entry": markdown2.markdown(entry).strip(),
        "title":title
        })

def random_rend(request):

    list = util.list_entries()
    if list:
        rand = random.choices(list)[0]
        return HttpResponseRedirect(reverse("wiki", args=(rand,)))
    
    return redirect(index)

def saveHandler(request, **kwargs):

    title = kwargs.get("title", "")
    content = kwargs.get("content", "")
    if content and title:
        title = title.strip()
        entry = util.save_entry(title.strip(), str(content).strip())
        return redirect("wiki", title=title)
    return redirect(notFound)


def create_update(request, title=""):

    dic = {"set": "create"}
    previous_title = title
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submit = request.POST.get("submit")
        hidden = request.POST.get("set")

        if submit is None:
            if "create" in hidden:
                return redirect(index)
            else:
                return redirect(reverse("wiki", kwargs={"title": title}))
        elif not title or not content:
    
            return render(request, "encyclopedia/create.html", dic)

        action = "updated" if "edit" in hidden else "created"
        if action == "updated":
            util.delete_entry(previous_title)
        
        return saveHandler(request, title=title, content=content)

    else:  
        dic = {"set": "create"}  
        if title:
            entry = util.get_entry(title)
            if not entry or entry is None:
                return redirect(notFound)
            dic["entry"] = entry
            dic["set"] = "edit"

        dic.update(
            {
                "title": title,
                "unavailable_entry": util.list_entries(),
            }
        )
    return render(request, "encyclopedia/create.html", dic)

def delete(request, title, deletion=None):

    if deletion:
        if title:
            if deletion == "delete":
                util.delete_entry(title)
                
                return redirect("index")
            else:
                
                return redirect("wiki", title=title)
            
def render(req, url, extra={}):

    alphabet_list = list(map(chr, range(65, 65 + 26)))
    extra.update(entries_options=util.list_entries(), 
    alphabet_list=alphabet_list,
    debug=settings.DEBUG)

    return _render(req, url, extra)



def notFound(request):
    return render(request, "encyclopedia/not-found.html")

