from random import choice, shuffle

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.urlresolvers import reverse
from django import forms
from django.http import Http404
from django.views.generic import TemplateView, FormView, CreateView

from .forms import SignUpForm, ReviewForm
from .mixins import PaginationMixin
from .models import Review, User, Announcement, Rules


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


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'
    form_class = ReviewForm
    login_url = '/users/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        reviews = request.user.reviews.order_by('created')
        context.update({'reviews': reviews})
        return self.render_to_response(context)


class CreateReview(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    success_url = '/users/account/'
    login_url = '/users/login/'

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        form = form_class(self.request.user, **kwargs)
        return form

    def form_valid(self, form):
        form.save()
        return super(CreateReview, self).form_valid(form)


class ReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'users/review.html'
    login_url = '/users/login/'

    def get(self, request, *args, **kwargs):
        review_id = kwargs.pop('review_id')
        try:
            review = Review.objects.get(pk=review_id, user=request.user)
        except Review.DoesNotExist:
            raise Http404
        context = self.get_context_data(**kwargs)
        context.update({'review': review})
        return self.render_to_response(context)


class PublicReviewView(TemplateView):
    template_name = 'summer_reading/public_review.html'

    def get(self, request, *args, **kwargs):
        review_id = kwargs.pop('review_id')
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            raise Http404
        context = self.get_context_data(**kwargs)
        context.update({'review': review})
        return self.render_to_response(context)


class AnnouncementView(TemplateView):
    template_name = 'summer_reading/announcement.html'

    def get(self, request, *args, **kwargs):
        announcement_id = kwargs.pop('announcement_id')
        try:
            announcement = Announcement.objects.get(pk=announcement_id)
        except Announcement.DoesNotExist:
            raise Http404
        context = self.get_context_data(**kwargs)
        context.update({'announcement': announcement})
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
        rules = Rules.objects.order_by('-modified').first()
        context = self.get_context_data(**kwargs)
        context.update({'reviews': reviews, 'announcements': announcements, 'rules': rules})
        return self.render_to_response(context)


class BrowseViewBase(PaginationMixin, TemplateView):
    template_name = None

    def set_browse_context(self, context, request, **kwargs):
        self.results_per_page = 25
        self.set_results()
        (paginator, page) = self.build_page(self.results, self.results_per_page)
        context.update({
            'page': page,
            'paginator': paginator,
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context = self.set_browse_context(context, request, **kwargs)
        return self.render_to_response(context)


class BrowseAnnouncements(BrowseViewBase):
    template_name = 'summer_reading/browse_announcements.html'

    def set_results(self):
        self.results = Announcement.objects.order_by('-created', '-modified')


class BrowsePublicReviews(BrowseViewBase, TemplateView):
    template_name = 'summer_reading/browse_public_reviews.html'

    def set_results(self):
        self.results = Review.objects.filter(make_public=True).order_by('-created', '-modified')
