from django.db import models
from django.contrib.auth.models import User
from PIL import Image #manipulacion de imagenes


def user_directory_path(instance, filename):
    # Guardará la imagen en: media/profile_pics/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default='profile_pics/default.png')


    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
           
        try: 
            old_profile = Profile.objects.get(pk=self.pk) 
            if old_profile.image != self.image and old_profile.image.name != 'profile_pics/default.png':
                old_profile.image.delete(save=False)
        except Profile.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            img.save(img_path)