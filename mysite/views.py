from django.template import loader



def custom404_view(request, exception):
    print("vao day")
    template = loader.get_template("templates/404.html")
    return render(request, "polls/index.html", context)
