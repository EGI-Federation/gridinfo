from django.db import models

class Entity(models.Model):
    uniqueid = models.CharField(max_length=255)
    type = models.CharField(max_length=96)
    timestamp = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=255,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    class Meta:
        unique_together = ("uniqueid", "type")
    def __unicode__(self):
        return '%s(%s)' % (self.uniqueid, self.type)

class Entityrelationship(models.Model):
    #subject = models.CharField(max_length=255)
    #object = models.CharField(max_length=255)
    subject= models.ForeignKey(Entity, related_name = 'subject')
    object = models.ForeignKey(Entity, related_name = 'object')
    predicate = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s : %s : %s' % (self.subject, self.predicate, self.object)