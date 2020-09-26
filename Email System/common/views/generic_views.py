from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from mysite.settings import EMAIL_HOST_USER as sender
from ..forms import SectionForm


def send_email(request):
    if not request.user.is_superuser:
        raise Http404

    if request.method == 'GET':
        form = SectionForm()
        return render(request, 'common/sender.html', {'form': form})

    if request.method == 'POST':
        emails = [user.email for user in User.objects.all() if user.email]
        subject, message = request.POST['subject'], request.POST['message']

        send_mail(
            subject,
            message,
            sender,
            emails,
        )

        return redirect('home')
