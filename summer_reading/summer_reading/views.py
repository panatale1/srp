from random import choice, shuffle

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, CreateView

from .forms import SignUpForm
from .models import Review, User


class SelectWinnersView(TemplateView):
    login_url = '/admin/login/'
    template_name = 'admin/select-winners.html'

    def post(self, request, *args, **kwargs):
        users = list(Review.objects.values_list('user', flat=True))
        for dummy in range(10):
            shuffle(users)
        winner = choice(users)
        context = self.get_context_data(**kwargs)
        context.update({'winner': winner})
        return self.render_to_response(context)


class UserRegisterView(CreateView):
    model = User
    form_class = SignUpForm

    def form_valid(self, form):
        response = super(UserRegisterView, self).form_valid(form)
        user = self.object
        import pdb; pdb.set_trace()
        authenticate(username=user.username, password=form.cleaned_data['password'])
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse('user-account')


class UserAccountView(TemplateView):
    template_name = 'users/account.html'

