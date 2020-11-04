from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import *
from .models import *
from .forms import *
from django.db import connection

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import datetime


def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')


def get_user(self):
    user_id = self.request.user.pk
    if user_id >= 2:
        return Employee.objects.get(pk=user_id)
    else:
        return False


class IndexView(ListView):
    queryset = object
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.pk == 1:
            context['keys'] = {'Post offices': 'post_offices', 'Publishing houses': 'publishing_houses',
                               'Regions': 'regions', 'Houses': 'houses', 'Publications': 'publications',
                               'Subscriptions': 'subscriptions', 'Followers': 'followers'}
        else:
            context['keys'] = {'Post offices': 'post_offices',
                               'Regions': 'regions', 'Houses': 'houses', 'Publications': 'publications',
                               'Subscriptions': 'subscriptions', 'Followers': 'followers'}
        return context


class PostOfficesView(ListView):
    Model = PostOffice
    context_object_name = 'post_offices'
    template_name = 'home/post_office_dir/post_offices.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post offices page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return PostOffice.objects.all().filter(pk=employee.post_office_id)
        else:
            return PostOffice.objects.all()


class PostOfficeByIdView(PostOfficeMixin, DetailView):
    model = PostOffice
    context_object_name = 'post_office'
    template_name = 'home/post_office_dir/post_office.html'


class PublishingHousesView(ListView):
    Model = PublishingHouse
    context_object_name = 'publishing_houses'
    template_name = 'home/publishing_house_dir/publishing_houses.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publishing houses page'
        return context

    def get_queryset(self):
        return PublishingHouse.objects.all()


class PublishingHouseByIdView(PublishingHouseMixin, DetailView):
    model = PublishingHouse
    context_object_name = 'publishing_house'
    template_name = 'home/publishing_house_dir/publishing_house.html'


class RegionsView(ListView):
    Model = Region
    context_object_name = 'regions'
    template_name = 'home/region_dir/regions.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Regions page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Region.objects.all().filter(post_office_id=employee.post_office_id)
        else:
            return Region.objects.all()


class RegionByIdView(RegionMixin, DetailView):
    model = Region
    context_object_name = 'region'
    template_name = 'home/region_dir/region.html'


class HousesView(ListView):
    Model = House
    context_object_name = 'houses'
    template_name = 'home/house_dir/houses.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Houses page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return House.objects.all().filter(region__post_office_id=employee.post_office_id)
        else:
            return House.objects.all()


class HouseByIdView(HouseMixin, DetailView):
    model = House
    context_object_name = 'house'
    template_name = 'home/house_dir/house.html'


class PublicationsView(ListView):
    Model = Release
    context_object_name = 'publications'
    template_name = 'home/publication_dir/publications.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publications page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Release.objects.all().filter(post_office_id=employee.post_office_id)
        else:
            return Release.objects.all()


class PublicationByIdView(PublicationMixin, DetailView):
    model = Release
    context_object_name = 'publication'
    template_name = 'home/publication_dir/publication.html'


class SubscriptionsView(ListView):
    Model = Subscription
    context_object_name = 'subscriptions'
    template_name = 'home/subscription_dir/subscriptions.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subscriptions page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Subscription.objects.all().filter(release__post_office_id=employee.post_office_id)
        else:
            return Subscription.objects.all()


class SubscriptionByIdView(SubscriptionMixin, DetailView):
    model = Subscription
    context_object_name = 'subscription'
    template_name = 'home/subscription_dir/subscription.html'


class FollowersView(ListView):
    Model = Follower
    context_object_name = 'followers'
    template_name = 'home/follower_dir/followers.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Followers page'
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Follower.objects.all().filter(house__region__post_office_id=employee.post_office_id)
        else:
            return Follower.objects.all()


class FollowerByIdView(FollowerMixin, DetailView):
    model = Follower
    context_object_name = 'follower'
    template_name = 'home/follower_dir/follower.html'


class ReportView(ListView):
    Model = Region
    context_object_name = 'regions'
    template_name = 'home/report_dir/report.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = get_user(self)
        context['title'] = 'Report page'
        context['post_offices'] = PostOffice.objects.all()
        context['publications'] = Follower_Subscription.objects.all()
        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Region.objects.filter(post_office_id=employee.post_office_id)
        else:
            return Region.objects.all()


class PostmenView(ListView):
    Model = Employee
    context_object_name = 'postmen'
    template_name = 'home/employee_dir/manage_postmen.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Manage postmen page'

        return context

    def get_queryset(self):
        employee = get_user(self)
        if employee:
            return Employee.objects.filter(position__name='Postman').filter(post_office_id=employee.post_office_id)
        else:
            return Employee.objects.all().filter(position__name='Postman')


class CreatePostmanView(CreateView):
    form_class = PostmanForm
    template_name = 'home/employee_dir/add_postman.html'
    success_url = reverse_lazy('manage_postmen')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new postman'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = get_user(self)
        return kwargs


class EditPostmanView(UpdateView):
    model = Employee
    form_class = PostmanForm
    template_name = 'home/employee_dir/edit_postman.html'
    success_url = reverse_lazy('manage_postmen')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = get_user(self)
        return kwargs


class DeletePostmanView(DeleteView):
    model = Employee
    template_name = 'home/employee_dir/confirm_delete_postman.html'
    success_url = reverse_lazy('manage_postmen')


def get_publications(request):
    if request.method == 'POST':
        post_office_name = request.POST.get("post_office_name")
        with connection.cursor() as c:
            c.callproc('get_post_office_publications', [post_office_name])
            results = c.fetchall()
        count = len(results)
        context = {'post_office': post_office_name, 'results': results, 'count': count, 'title': 'Query result'}
        return render(request, 'home/queries_dir/query_2/result.html', context)
    else:
        query_form = PostOfficePublicationsQueryForm()
        post_offices = PostOffice.objects.all()
        employee = Employee.objects.get(pk=request.user.pk) if request.user.pk >= 2 else False
        if employee:
            query_form.fields['post_office_name'].choices = [(name.name, name.name) for
                                                             name in post_offices.filter(pk=employee.post_office_id)]
        else:
            query_form.fields['post_office_name'].choices = [(name.name, name.name) for
                                                             name in post_offices]

        context = {'form': query_form, 'title': 'Get all publications of the post office'}
        return render(request, 'home/queries_dir/query_2/query.html', context)


def get_postmen(request):
    if request.method == 'POST':
        post_office_name = request.POST.get("post_office_name")
        with connection.cursor() as c:
            c.callproc('get_post_office_postmen ', [post_office_name])
            results = c.fetchall()
        count = len(results)
        context = {'post_office': post_office_name, 'postmen': results, 'count': count, 'title': 'Query result'}
        return render(request, 'home/queries_dir/query_1/result.html', context)
    else:
        query_form = PostOfficePublicationsQueryForm()
        post_offices = PostOffice.objects.all()
        employee = Employee.objects.get(pk=request.user.pk) if request.user.pk >= 2 else False
        if employee:
            query_form.fields['post_office_name'].choices = [(name.name, name.name) for
                                                             name in post_offices.filter(pk=employee.post_office_id)]
        else:
            query_form.fields['post_office_name'].choices = [(name.name, name.name) for
                                                             name in post_offices]
        context = {'form': query_form, 'title': 'Get count of the postmen of the post office'}
        return render(request, 'home/queries_dir/query_1/query.html', context)


def get_served_address(request):
    if request.method == 'POST':
        address = request.POST.get("address")
        with connection.cursor() as c:
            c.callproc('get_postman_of_served_address ', [address])
            results = c.fetchall()
        count = len(results)
        context = {'address': address, 'count': count, 'proc': results, 'title': 'Query result'}
        return render(request, 'home/queries_dir/query_3/result.html', context)
    else:
        query_form = PostmanAddressForm()
        addresses = House.objects.all()
        employee = Employee.objects.get(pk=request.user.pk) if request.user.pk >= 2 else False
        if employee:
            query_form.fields['address'].choices = [(address.address, address.address) for address in
                                                    addresses.filter(region__post_office_id=employee.post_office_id)]
        else:
            query_form.fields['address'].choices = [(address.address, address.address) for address in addresses]
        context = {'form': query_form, 'title': 'Get the name of the postman to the address'}
        return render(request, 'home/queries_dir/query_3/query.html', context)


def get_follower_publication(request):
    if request.method == 'POST':
        follower = request.POST.get("followers")
        follower_split = follower.split(' ')
        with connection.cursor() as c:
            c.callproc('get_follower_publications ', [follower_split[0], follower_split[1], follower_split[2]])
            results = c.fetchall()
        count = len(results)
        context = {'follower': follower, 'proc': results, 'count': count, 'title': 'Query result'}
        return render(request, 'home/queries_dir/query_4/result.html', context)
    else:
        query_form = FollowerForm()
        followers = Follower.objects.all()
        employee = Employee.objects.get(pk=request.user.pk) if request.user.pk >= 2 else False
        if employee:
            query_form.fields['followers'].choices = [(follower, follower) for follower in followers.filter(
                house__region__post_office_id=employee.post_office_id)]
        else:
            query_form.fields['followers'].choices = [(follower, follower) for follower in followers]
        context = {'form': query_form, 'title': 'Get follower''s publications'}
        return render(request, 'home/queries_dir/query_4/query.html', context)


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename-Expenses' + \
                                      str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    if request.user.pk >= 2:
        regions = Region.objects.filter(post_office_id=Employee.objects.get(pk=request.user.pk).post_office_id)
    else:
        superuser = True
        regions = Region.objects.all()

    html_string = render_to_string('home/report_dir/pdf-output.html', {'regions': regions, 'superuser': superuser})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'home/authorization/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
