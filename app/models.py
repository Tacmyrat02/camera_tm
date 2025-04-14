from django.db import models

class IPCamera(models.Model):
    
    model_name = models.CharField(max_length=255)
    features = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/cameras/')  # You'll need to install Pillow for image handling

    def __str__(self):
        return self.model_name

class HomePhone(models.Model):
    model_name = models.CharField(max_length=255)
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_handsets = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/phones/')  # You'll need to install Pillow for image handling

    def __str__(self):
        return self.model_name

class CartItem(models.Model):

    camera = models.ForeignKey(IPCamera, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100)  # sessiýa bilen baglanyşykly

    def __str__(self):
        return f"{self.camera.model_name} ({self.quantity})"
class NVR(models.Model):
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    channels = models.IntegerField()
    storage_capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.model_name
from django.db import models

class Switch(models.Model):
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    ports = models.IntegerField()  # Number of ports
    speed = models.CharField(max_length=50)  # Speed (e.g., 1Gbps, 10Gbps)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.brand} {self.model_name}"
from django.db import models

class HardDisk(models.Model):
    storage_capacity = models.PositiveIntegerField()  # Capacity in GB
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the hard disk
    description = models.TextField(blank=True, null=True)  # Optional description of the hard disk

    def __str__(self):
        return f"{self.storage_capacity}GB - ${self.price}"
