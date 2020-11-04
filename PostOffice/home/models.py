from datetime import date, timedelta

from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.db.models import *


class PostOffice(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    address = models.CharField(verbose_name='Address', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post office'
        verbose_name_plural = 'Post offices'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_post_office', kwargs={'pk': self.pk})


class Position(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50, unique=True)
    salary = models.DecimalField(verbose_name='Salary', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['pk']


class Employee(models.Model):
    first_name = models.CharField(verbose_name='First name', max_length=50)
    last_name = models.CharField(verbose_name='Last name', max_length=50)
    middle_name = models.CharField(verbose_name='Middle name', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=80, unique=True, default='someworkmail@gmail.com')
    phone = PhoneNumberField(verbose_name='Telephone number', unique=True, default='+375333215378')
    position = models.ForeignKey('Position', on_delete=models.PROTECT, default=1)
    post_office = models.ForeignKey('PostOffice', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_employee', kwargs={'pk': self.pk})


class PublishingHouse(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50, unique=True)
    address = models.CharField(verbose_name='Address', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Publishing House'
        verbose_name_plural = 'Publishing Houses'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_publishing_house', kwargs={'pk': self.pk})


class Publication(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50, unique=True)
    publishing_house = models.ForeignKey('PublishingHouse', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_publication', kwargs={'pk': self.pk})


class Release(models.Model):
    price = models.DecimalField(verbose_name='Price', max_digits=9, decimal_places=2)
    count = models.PositiveIntegerField(verbose_name='Count', default=1)
    publication = models.ForeignKey('Publication', on_delete=models.PROTECT)
    post_office = models.ForeignKey('PostOffice', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.publication.pk}, {self.publication.name}'

    class Meta:
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'
        ordering = ['pk']


class Region(models.Model):
    index = models.PositiveIntegerField(verbose_name='Region Index', unique=True)
    post_office = models.ForeignKey('PostOffice', on_delete=models.PROTECT)
    postman = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.index}'

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_region', kwargs={'pk': self.pk})


class House(models.Model):
    address = models.CharField(verbose_name='Address', max_length=100, unique=True)
    region = models.ForeignKey('Region', on_delete=models.PROTECT)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_house', kwargs={'pk': self.pk})


class Follower(models.Model):
    first_name = models.CharField(verbose_name='First name', max_length=50)
    last_name = models.CharField(verbose_name='Last name', max_length=50)
    middle_name = models.CharField(verbose_name='Middle name', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=80, unique=True, default='somemail@gmail.com')
    phone = PhoneNumberField(verbose_name='Telephone number', unique=True, default='+375333215678')
    house = models.ForeignKey('House', on_delete=models.PROTECT)
    subscription = models.ManyToManyField('Subscription', through='Follower_Subscription')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_follower', kwargs={'pk': self.pk})


class Follower_Subscription(models.Model):
    follower = models.ForeignKey('Follower', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower.last_name}\n{self.subscription.end_date}'

    class Meta:
        verbose_name = 'Follower and Subscription'
        verbose_name_plural = 'Followers and Subscriptions'
        ordering = ['pk']


class Subscription(models.Model):
    start_date = models.DateField(verbose_name='Subscription started', default=date.today)
    description = models.TextField(verbose_name='Description', unique=True)
    term = models.PositiveSmallIntegerField(verbose_name='Subscription term(month)', default=1)
    end_date = models.DateField(verbose_name='Subscription end', default=date.today() + timedelta(30))
    release = models.ForeignKey('Release', on_delete=models.PROTECT)

    def __str__(self):
        return f'Post office: {self.release.post_office}, Publication id: {self.release.pk},Name: {self.release.publication.name:}, term: {self.term} month, ' \
               f'count of publications:{self.release.count}'

    def total_price(self):
        return self.release.price * self.term

    def save(self, *args, **kwargs):
        self.end_date = timedelta(self.term * 30) + self.start_date
        super(Subscription, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('view_subscription', kwargs={'pk': self.pk})
