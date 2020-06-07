from django.utils import timezone
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
    return F"{pre_url}/{instance.profile.id}/bio/ab_{date}{filename}"


def AuthorImage(instance, filename):
    return F"{pre_url}/{instance.profile.id}/bio/ai_{date}{filename}"


def PostBanner(instance, filename):
    return F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pb_{filename}"


def PostImage(instance, filename):
    return F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pi_{filename}"


def MorePostImage(instance, filename):
    return F"{pre_url}/{instance.post.author.profile.id}/posts/{instance.post.title}/mpi_{filename}"
