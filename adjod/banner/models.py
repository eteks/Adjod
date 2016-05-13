from django.db import models
from adjod.models import UserProfile
from core.extra import ContentTypeRestrictedFileField
from datetime import timedelta,datetime

POSITION = (
    ('Top', 'Top of the page'),
    ('Bottom', 'Bottom of the page'),
    # ('Center', 'Center of the page'),
    ('Center_top', 'Center top of the page'),
    ('Center_bottom', 'Center bottom of the page'),
    ('Right', 'Right of the page'),
    ('Right_top', 'Right top of the page'),
    ('Right_bottom', 'Right bottom of the page'),
    ('Left', 'Left of the page'),
    ('Background_Right', 'Backgorund Right of the page'),
    ('Background_Left', 'Backgorund Left of the page'),
)

PAGEURL = (
    ('Home page', 'Home page'),
    ('Listing page', 'Listing page'),
    ('Details page', 'Details page'),
)

BANNERTYPE = (
    ('Own', 'Own Banner'),
    ('Other', 'Other Banner'),
)


class BannerPosition(models.Model):
    position = models.CharField(max_length=50, help_text='Enter position of the banner for your site', unique=True)

    def __unicode__(self):
        return unicode(self.position)

class BannerPlan(models.Model):
    page = models.CharField(max_length=50, choices=PAGEURL,help_text='Choose which page you want show your banner')
    position = models.CharField(max_length=50, choices=POSITION,help_text='Choose position of your banner')
    price = models.FloatField(null=True, default=0.0,help_text='Amount of the banner based on page and position')
    plan_duration = models.BigIntegerField(
        null=True, help_text="No of days allowed")
    bannertype = models.CharField(max_length=50, choices=BANNERTYPE, help_text='Choose BannerType of your banner')
    height = models.BigIntegerField(
        null=True, blank=True, help_text="Please enter the height to be allowed for this banner plan")
    width = models.BigIntegerField(
        null=True, blank=True, help_text="Please enter the width to be allowed for this banner plan")
    class Meta:
        unique_together = (("page", "position", "bannertype"), ("page", "position"))

    def __unicode__(self):
        return unicode(self.page+' '+self.position+' '+self.bannertype)


class PostBanner(models.Model):
    # user = models.ForeignKey(UserProfile, null=True, blank=True,help_text='Choose which user post banner in site')
    banner = ContentTypeRestrictedFileField(upload_to='banners',
        content_types=['image/jpg','image/jpeg', 'image/png','image/gif'], max_upload_size=2097152,
        help_text="Please upload the banner Image with 2MB min and jpg, jpeg, png \
        , gif format only allowed", null=True, blank=True)
    # source = models.CharField(max_length=500, null=True,
    #                         blank=True,
    #                         help_text="Please enter the source for API banners")
    source = models.TextField(null=True,
                            blank=True,
                            help_text="Please enter the source for API banners")
    link = models.CharField(max_length=200, blank = True,
                            help_text="Please enter website redirect link for the banner")
    bannerplan = models.ForeignKey(BannerPlan,help_text='Choose bannerplan',verbose_name="Banner Plan")
    startdate = models.DateTimeField(
        default=datetime.now(), help_text="Start date for banner",verbose_name="Start Date")
    enddate = models.DateTimeField(default=datetime.now(
    ) + timedelta(days=30), help_text="End date for banner",verbose_name="End Date")
    admin_status = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.banner)
