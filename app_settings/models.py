from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Sum, FloatField
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class NewLevels(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    help_links = models.TextField(null=True, blank=True, default='')
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='levelslist')

    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('levels_home')

    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round(completed_count / total_count * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    ## display 
    def children(self):
        return NewLevels.objects.filter(parent=self.pk, active=True)
    def serializable_object(self):
        obj = {'title': self.title, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj