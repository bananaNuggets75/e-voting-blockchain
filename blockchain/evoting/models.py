from django.db import models
import hashlib
import json
from datetime import datetime
from django.contrib.auth.models import User

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.party})"

class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter} voted for {self.candidate}"

class Block(models.Model):
    index = models.IntegerField()
    vote_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        """Generate hash before saving"""
        block_string = json.dumps({
            "index": self.index,
            "vote_data": self.vote_data,
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash,
        }, sort_keys=True).encode()

        self.hash = hashlib.sha256(block_string).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.index} - Hash: {self.hash[:10]}..."
