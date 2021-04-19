from django.shortcuts import render, redirect
from .forms import AddLinkForm
from .models import Link


def home_view(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == "POST":
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Error Occured! Coudn't get the data for the url."
        except:
            error = "Something went wrong!"

    form = AddLinkForm()

    links = Link.objects.all().order_by("created")
    items_no = links.count()

    if items_no > 0:
        discount_list = []
        for item in links:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_discounted = len(discount_list)

    context = {
        "links": links,
        "items_no": items_no,
        "no_discounted": no_discounted,
        "form": form,
        "error": error,
    }

    return render(request, "links/main.html", context)


def update_items(request):
    links = Link.objects.all()
    for link in links:
        link.save()
    return redirect("home")
