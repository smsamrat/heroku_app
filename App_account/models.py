from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MyAccountsManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise username('Users must have an email address')
        if not email:
            raise ValueError('Users must have an username')

        user = self.model(
        email=self.normalize_email(email),
        username = username,
        first_name = first_name,
        last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name =  models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    username =  models.CharField(max_length=50, unique=True)
    email =  models.EmailField(max_length=50, unique=True)
    phone_number =  models.CharField(max_length=50)


    #requird
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # here is_active should be to for normal user to access home page after login
    is_superadmin = models.BooleanField(default=False)

    objects = MyAccountsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name'] #required field should be include to usercreation form if not requeired then not need to include

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')
    username = models.CharField(max_length=200, blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    address_1 = models.TextField(blank=True)
    city = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False

        return True

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile_pic')
    images = models.ImageField(upload_to="profile_pics")

