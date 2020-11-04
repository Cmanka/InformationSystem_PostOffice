from django.db.models import Count
from django.views.generic.detail import ContextMixin, SingleObjectMixin

from home.models import *


class PostOfficeMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Post office {self.kwargs["pk"]}'
        context['employees'] = PostOffice.objects.get(pk=self.kwargs["pk"]).employee_set.all()
        context['postmen'] = PostOffice.objects.get(pk=self.kwargs["pk"]).employee_set.annotate(
            cnt=Count('post_office')).filter(
            position__name='Postman')
        context['operators'] = PostOffice.objects.get(pk=self.kwargs["pk"]).employee_set.annotate(
            cnt=Count('post_office')).filter(
            position__name='Operator')
        context['regions'] = PostOffice.objects.get(pk=self.kwargs["pk"]).region_set.all()
        context['publications'] = PostOffice.objects.get(pk=self.kwargs["pk"]).release_set.all()
        return context


class PublishingHouseMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Publishing house {self.kwargs["pk"]}'
        context['publications'] = PublishingHouse.objects.get(pk=self.kwargs["pk"]).publication_set.all()
        return context


class RegionMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Region {self.kwargs["pk"]}'
        context['houses'] = Region.objects.get(pk=self.kwargs["pk"]).house_set.all()
        return context


class HouseMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'House {self.kwargs["pk"]}'
        context['people'] = House.objects.get(pk=self.kwargs["pk"]).follower_set.all()
        return context


class PublicationMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Publication {self.kwargs["pk"]}'
        return context


class SubscriptionMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Subscription {self.kwargs["pk"]}'
        context['total_price'] = Subscription.objects.get(
            pk=self.kwargs["pk"]).release.price * Subscription.objects.get(pk=self.kwargs["pk"]).term
        return context


class FollowerMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Follower {self.kwargs["pk"]}'
        context['subscriptions'] = Follower.objects.get(pk=self.kwargs["pk"]).subscription.all()
        context['postman'] = Follower.objects.get(pk=self.kwargs["pk"]).house.region.postman
        return context


class ReportMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Report'
        return context
