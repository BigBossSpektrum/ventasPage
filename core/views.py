from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'product_list.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def send_contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Nombre: {name}\nCorreo: {email}\n\n{message}"
        try:
            send_mail(subject, full_message, 'LagoTech Innovations', ['silvekerhernandez@gmail.com'], fail_silently=False)
            messages.success(request, '¡Tu mensaje fue enviado exitosamente!')
        except Exception as e:
            messages.error(request, 'Hubo un problema al enviar tu mensaje. Inténtalo de nuevo.')

        return redirect('contact')