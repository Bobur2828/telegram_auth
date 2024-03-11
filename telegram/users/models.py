from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
from datetime import datetime, timedelta
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

# AUTH steps
REGULAR,SUPPORT,ADMIN=('regular','support','admin')
NEW,CODE_VERIFIED,DONE,IMAGE_STEP=('new','code_verified','done','image_step')

# User register type

UZB,KOR,KAZ,AME,RUS=('UZBEKISTAN','KOREA','KAZAKHSTAN','AMERICA','RUSSIA')

class User(BaseModel,AbstractUser):
    USER_ROLES = (
        (REGULAR,REGULAR),
        (SUPPORT,SUPPORT),
        (ADMIN,ADMIN)
    )

    AUTH_STEPS_CHOICES = (
        (NEW,NEW),
        (CODE_VERIFIED,CODE_VERIFIED),
        (DONE,DONE),
        (IMAGE_STEP,IMAGE_STEP)
    )

    AUTH_COUNTRY_CHOICES = (
        (UZB, UZB),
        (KOR, KOR),
        (KAZ, KAZ),
        (AME, AME),
        (RUS, RUS),
    )

    auth_country = models.CharField(max_length=20, choices=AUTH_COUNTRY_CHOICES)
    auth_status=models.CharField(max_length=20, choices=AUTH_STEPS_CHOICES, default=NEW)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default=REGULAR)
    phone_number=models.CharField(max_length=13, unique=True, null=True,blank=True)
    email=models.CharField(max_length=254, unique=True, null=True,blank=True)
    image=models.ImageField(upload_to='user_images', null=True, blank=True)
    bio=models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username    
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def check_username(self):
        if not self.username:
            temp_username=f"telegram-{str(uuid.uuid4()).split('-')[-1]}"

            while User.objects.filter(username=temp_username).exists():
                temp_username=f"{temp_username}{random.randint(0,100)}"

            self.username=temp_username
    
    def check_pass(self):
        if not self.password:
            temp_password = f"telegram-{str(uuid.uuid4()).split('-')[-1]}"
            self.password = temp_password
    
    def check_hash_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

    def save(self,*args, **kwargs):
        self.check_username()
        self.check_pass()
        self.check_hash_password()
        super(User,self).save(*args, **kwargs)

    # def create_code_confirmation(self):


class UserCodeVerification(BaseModel):
    AUTH_COUNTRY_CHOICES = (
        (UZB, UZB),
        (KOR, KOR),
        (KAZ, KAZ),
        (AME, AME),
        (RUS, RUS),
    )
    auth_country=models.CharField(max_length=20,choices=AUTH_COUNTRY_CHOICES)
    code=models.CharField(max_length=6)
    is_confirmed=models.BooleanField(default=False)
    expire_time=models.DateTimeField(null=True) 
    user = models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='confirmation_codes')

    def __str__(self):
        return f"{self.user.username}{self.code}"
    
    def save(self, *args, **kwargs):
        if self.auth_type in [UZB, KOR, KAZ, AME, RUS]:
            self.expire_time = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)
