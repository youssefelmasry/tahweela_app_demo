from django.db import models

class Rate(models.Model):
    """A model represinting Currency Exchange Rates on a specific day"""

    base = models.CharField(max_length=3)
    date = models.DateField()
    rates = models.JSONField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        """A unicode representation of Rate model"""
        return f"{self.pk}"

class BaseCurrencies(models.Model):
    """A model representing all available currencies"""
    currency = models.CharField(max_length=3)

    def __str__(self):
        """A unicode representation of BaseCurrencies model"""
        return self.currency