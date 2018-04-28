from random import choice, shuffle

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django import forms
from django.views.generic import TemplateView, FormView, CreateView

from .forms import SignUpForm, ReviewForm
from .models import Review, User, Announcement


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
        authenticate(username=user.username, password=form.cleaned_data['password'])
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse('user-account')


class UserAccountView(TemplateView):
    template_name = 'users/account.html'
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        reviews = request.user.reviews.order_by('created')
        context.update({'reviews': reviews})
        return self.render_to_response(context)

class CreateReview(CreateView):
    model = Review
    form_class = ReviewForm
    success_url = '/users/account/'

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        form = form_class(self.request.user, **kwargs)
        return form

    def form_valid(self, form):
        form.save()
        return super(CreateReview, self).form_valid(form)


class ReviewView(TemplateView):
    template_name = 'users/review.html'

    def get(self, request, *args, **kwargs):
        review_id = kwargs.pop('review_id')
        review = Review.objects.get(pk=review_id)
        context = self.get_context_data(**kwargs)
        context.update({'review': review})
        return self.render_to_response(context)


class HomeView(TemplateView):
    template_name = 'summer_reading/home.html'

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.filter(make_public=True).order_by('-created')
        if reviews.count() > 10:
            reviews = reviews[:10]
        announcements = Announcement.objects.order_by('-created')
        if announcements.count() > 10:
            announcements = announcements[:10]
        context = self.get_context_data(**kwargs)
        context.update({'reviews': reviews, 'announcements': announcements})
        return self.render_to_response(context)
