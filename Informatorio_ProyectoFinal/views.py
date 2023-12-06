from django.shortcuts import render

def Home(request): 

    return render(request, 'home.html')

def About(request): 

    return render(request, 'about.html')

def Contacto(request): 

    return render(request, 'contact.html')

def Post(request): 

    return render(request, 'post.html')
    