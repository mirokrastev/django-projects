from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.views import View


class Home(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return self.home_page('Content here')
        if self.request.user.is_superuser:
            content = {'all_emails': [user.email for user in User.objects.all() if user.email]}
            return render(self.request, 'superuser_template.html', content)
        return self.__auth_action()

    def post(self, request):
        if not self.request.user.is_authenticated:
            return self.home_page('Unauthorized action!')

        user = User.objects.get(username=self.request.user)
        if self.request.user.email:
            user.email = ''
            user.save()
            return redirect('home')

        email = self.request.POST['email']

        try:
            validate_email(email)
        except ValidationError as message:
            return self.home_page(message.message)

        user.email = email
        user.save()
        return redirect('home')

    def __auth_action(self):
        email = User.objects.get(username=self.request.user).email
        if not email:
            message = 'You don\'t have email address in the database.'
        else:
            message = f'Your email is {email}'

        return self.home_page(message)

    def home_page(self, message=None):
        return render(self.request, 'home.html', {'message': message})
