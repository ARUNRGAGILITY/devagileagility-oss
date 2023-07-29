from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class RegCode(models.Model):
    reg_code = models.CharField(max_length=250, default='a1A1B1B2C1C3N4', null=False, blank=False)
    
    def __str__(self):
        return str(self.reg_code)