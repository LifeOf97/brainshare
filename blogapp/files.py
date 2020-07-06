from django.utils import timezone
import subprocess
import pathlib
"""
The functions in these module are used to direct where uploaded
files are to be stored. files will have a date in the it the
format will be 
for author bio banners = 'authorid/bio/bb_DDMMYYYY/filename'
for author bio mugshots = 'authorid/bio/bi_DDMMYYYY/filename'
for author post banners = 'authorid/posts/posttitle/pb_filename'
for author post images = 'authorid/posts/posttitle/pi_filename'
for author morepost image = 'authorid/posts/posttitle/mpi_filename'
"""

now = timezone.now()
date = now.strftime(F"%d%m%Y")
pre_url = 'blogapp/authors'


def AuthorBanner(instance, filename):
    location = F"{pre_url}/{instance.profile.id}/bio/ab_{date}{filename}"
    return location


def AuthorImage(instance, filename):
    location = F"{pre_url}/{instance.profile.id}/bio/ai_{date}{filename}"
    return location


def PostBanner(instance, filename):
    location = F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pb_{filename}"
    return location


def PostImage(instance, filename):
    location = F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pi_{filename}"
    return location


def MorePostImage(instance, filename):
    location = F"{pre_url}/{instance.post.author.profile.id}/posts/{instance.post.title}/mpi_{filename}"
    return location
