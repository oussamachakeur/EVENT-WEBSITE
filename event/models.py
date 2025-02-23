from django.db import models
from django.contrib.auth.models import User
from datetime import date 

class Venue(models.Model):
    name= models.CharField('name of venue' , max_length=100 , null=False)
    address= models.CharField('address' , max_length=100 , null=False)
    zip_code = models.CharField('zip' , max_length=10) 
    phone= models.CharField('phone number' , max_length=15 , blank=True)
    web= models.URLField('website url' , blank= True)
    email = models.EmailField('email' , blank=True)
    owner = models.IntegerField('Venue Owner' , blank= False , default=1)
    image = models.ImageField(null= True , blank=True , upload_to='images/')

    def __str__(self):
        return self.name

class MyUser(models.Model):
    first_name =models.CharField('first name ' ,max_length=100 , null=False)
    last_name= models.CharField('last name ' ,max_length=100 , null=False)
    email= models.EmailField('email')

    def __str__(self):
        return self.first_name + '' + self.last_name


class Event(models.Model):
    name = models.CharField('event name' , max_length=100 , null= False)
    date = models.DateField('event date')
    venue = models.ForeignKey(Venue ,null=True , on_delete=models.CASCADE )
    #venue = models.CharField('event venue', max_length=100, null=False)
    #manager = models.CharField('manager' , max_length=100 )
    manager = models.ForeignKey(User, null=True , on_delete= models.SET_NULL)
    description = models.TextField('description' , null= True)
    attendees = models.ManyToManyField(MyUser)
    approved = models.BooleanField('approved' , default=False)


    def __str__(self):
        return self.name


    @property
    def days_till(self):
        today = date.today()
        days_till = self.date - today 
        days_till_stripped = str(days_till).split(',',1)[0]
        return days_till_stripped
