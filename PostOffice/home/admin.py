from django.contrib import admin
from django.core.checks import messages
from django.core.mail import send_mail
from django import forms

from .models import *


class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    list_display_links = ('id', 'name', 'address')
    search_fields = ('name',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary')
    list_display_links = ('id', 'name', 'salary')
    search_fields = ('name', 'id')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'middle_name', 'email', 'phone', 'position', 'post_office')
    list_display_links = (
        'id', 'first_name', 'last_name', 'middle_name', 'email', 'phone', 'position', 'post_office')
    search_fields = ('lastName', 'email', 'id')
    initial_fields = ['first_name', 'last_name', 'middle_name', 'email', 'phone', 'position', 'post_office']

    def get_queryset(self, request):
        qs = super(EmployeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id).exclude(
            position__name='Manager')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'post_office':
            if queryset is None:
                queryset = PostOffice.objects.all()
            if request.user.is_superuser:
                queryset = PostOffice.objects.all()
            else:
                queryset = queryset.filter(pk=Employee.objects.get(pk=request.user.pk).post_office_id)
        if db_field.name == 'position':
            if queryset is None:
                queryset = Position.objects.all()
            if request.user.is_superuser:
                queryset = Position.objects.all()
            else:
                queryset = queryset.exclude(name='Manager')

        return queryset


class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    list_display_links = ('id', 'name', 'address')
    search_fields = ('name', 'id')


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publishing_house')
    list_display_links = ('id', 'name', 'publishing_house')
    search_fields = ('name', 'id')


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'count', 'publication', 'post_office')
    list_display_links = ('id', 'price', 'count', 'publication', 'post_office')
    search_fields = ('price', 'id', 'count')
    initial_fields = ['price', 'count', 'publication', 'post_office']

    def get_queryset(self, request):
        qs = super(ReleaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'post_office':
            if queryset is None:
                queryset = PostOffice.objects.all()
            if request.user.is_superuser:
                queryset = PostOffice.objects.all()
            else:
                queryset = queryset.filter(pk=Employee.objects.get(pk=request.user.pk).post_office_id)

        return queryset


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'postman', 'post_office')
    list_display_links = ('id', 'index', 'post_office', 'postman')
    search_fields = ('index', 'id')
    initial_fields = ['index', 'postman', 'post_office']

    def get_queryset(self, request):
        qs = super(RegionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'postman':
            if queryset is None:
                queryset = Employee.objects.all()
            if request.user.is_superuser:
                queryset = Employee.objects.all()
            else:
                queryset = queryset.filter(
                    post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id).filter(
                    position__name='Postman')
        if db_field.name == 'post_office':
            if queryset is None:
                queryset = PostOffice.objects.all()
            if request.user.is_superuser:
                queryset = PostOffice.objects.all()
            else:
                queryset = queryset.filter(pk=Employee.objects.get(pk=request.user.pk).post_office_id)

        return queryset


class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'region')
    list_display_links = ('id', 'address', 'region')
    search_fields = ('address', 'id')
    initial_fields = ['address', 'region']

    def get_queryset(self, request):
        qs = super(HouseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'region':
            if queryset is None:
                queryset = Region.objects.all()
            if request.user.is_superuser:
                queryset = Region.objects.all()
            else:
                queryset = queryset.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

        return queryset


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'phone', 'house')
    list_display_links = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'phone', 'house')
    search_fields = ('lastName', 'id', 'email')
    initial_fields = ['first_name', 'last_name', 'middle_name', 'email', 'phone', 'house']

    def get_queryset(self, request):
        qs = super(FollowerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(house__region__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'house':
            if queryset is None:
                queryset = House.objects.all()
            if request.user.is_superuser:
                queryset = House.objects.all()
            else:
                queryset = queryset.filter(
                    region__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

        return queryset


class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('start_date', 'term', 'description', 'release')
    initial_fields = ['start_date', 'term', 'description', 'release']
    list_display = ('id', 'start_date', 'term', 'end_date', 'description', 'release')
    list_display_links = ('id', 'start_date', 'term', 'end_date', 'description', 'release')
    search_fields = ('term', 'id',)

    def get_queryset(self, request):
        qs = super(SubscriptionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(release__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'release':
            if queryset is None:
                queryset = Release.objects.all()
            if request.user.is_superuser:
                queryset = Release.objects.all()
            else:
                queryset = queryset.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)
        return queryset


class SubFollAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'subscription')
    initial_fields = ['follower', 'subscription']

    def get_queryset(self, request):
        qs = super(SubFollAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            follower__house__region__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = self.initial_fields
        return fields

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'follower':
            if queryset is None:
                queryset = Follower.objects.all()
            if request.user.is_superuser:
                queryset = Follower.objects.all()
            else:
                queryset = queryset.filter(
                    house__region__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)
        if db_field.name == 'subscription':
            if queryset is None:
                queryset = Subscription.objects.all()
            if request.user.is_superuser:
                queryset = Subscription.objects.all()
            else:
                queryset = queryset.filter(
                    release__post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)
        return queryset

    def save_model(self, request, obj, form, change):
        mail = send_mail('Subscribing',
                         f'Total price:{obj.subscription.total_price()}$\n'
                         f'Term:{obj.subscription.term} month\n'
                         f'Publication:{obj.subscription.release.publication.name}\n'
                         f'Description:{obj.subscription.description}',
                         'andrewlabun934@gmail.com',
                         [f'{obj.follower.email}', 'offatrubkin@gmail.com'],
                         fail_silently=False)
        if mail:
            print('success')
            obj.save()
        else:
            print('error')


admin.site.register(PostOffice, PostOfficeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PublishingHouse, PublishingHouseAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Follower_Subscription, SubFollAdmin)

admin.site.site_header = 'Information system'
admin.site.site_title = 'Manage information system'
