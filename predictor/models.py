from django.db import models

# Create your models here.
from django.db import models

class QoSInput(models.Model):
    signal_strength = models.FloatField()
    required_bandwidth = models.FloatField()
    allocated_bandwidth = models.FloatField()
    resource_allocation = models.FloatField()
    cpu_utilization = models.FloatField()
    memory_utilization = models.FloatField()
    distance_from_bs = models.FloatField()

    SLICE_TYPE_CHOICES = [
        ('URLLC', 'URLLC'),
        ('eMBB', 'eMBB')
    ]
    slice_type = models.CharField(max_length=10, choices=SLICE_TYPE_CHOICES)

    APPLICATION_TYPE_CHOICES = [
        ('Background_Download', 'Background Download'),
        ('Emergency_Service', 'Emergency Service'),
        ('File_Download', 'File Download'),
        ('IoT_Temperature', 'IoT Temperature'),
        ('Online_Gaming', 'Online Gaming'),
        ('Streaming', 'Streaming'),
        ('Video_Call', 'Video Call'),
        ('Video_Streaming', 'Video Streaming'),
        ('VoIP_Call', 'VoIP Call'),
        ('Voice_Call', 'Voice Call'),
        ('Web_Browsing', 'Web Browsing')
    ]
    application_type = models.CharField(max_length=30, choices=APPLICATION_TYPE_CHOICES)

    SLICE_PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Low', 'Low')
    ]
    slice_priority = models.CharField(max_length=10, choices=SLICE_PRIORITY_CHOICES)

    TIME_OF_DAY_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening')
    ]
    time_of_day = models.CharField(max_length=10, choices=TIME_OF_DAY_CHOICES)

    WEATHER_CONDITIONS_CHOICES = [
        ('Cloudy', 'Cloudy'),
        ('Rainy', 'Rainy'),
        ('Sunny', 'Sunny')
    ]
    weather_conditions = models.CharField(max_length=10, choices=WEATHER_CONDITIONS_CHOICES)

    USER_MOBILITY_CHOICES = [
        ('Driving', 'Driving'),
        ('Stationary', 'Stationary'),
        ('Walking', 'Walking')
    ]
    user_mobility = models.CharField(max_length=15, choices=USER_MOBILITY_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)  # To track when the input was provided

class QoSPrediction(models.Model):
    input_data = models.OneToOneField(QoSInput, on_delete=models.CASCADE)  # Link to the input
    latency = models.FloatField()
    jitter = models.FloatField()
    throughput = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # To track when the prediction was made
