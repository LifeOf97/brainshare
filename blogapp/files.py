from django.utils import timezone
"""
The functions in these module are used to direct where uploaded
files are to be stored. files will be stored with date prefixing
the full name. The date will be following the 'DDMMYY' format
NOTE: ab, ai, pb, pi, mpi are abbrevations of their function names.
"""

now = timezone.now()
date = now.strftime(F"%d%m%Y")
pre_url = 'blogapp/authors'


def AuthorBanner(instance, filename):
    return F"{pre_url}/{instance.profile.id}/bio/ab{date}{filename}"


def AuthorImage(instance, filename):
    return F"{pre_url}/{instance.profile.id}/bio/ai{date}{filename}"


def PostBanner(instance, filename):
    return F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pb_{filename}"


def PostImage(instance, filename):
    return F"{pre_url}/{instance.author.profile.id}/posts/{instance.title}/pi_{filename}"


def MorePostImage(instance, filename):
    return F"{pre_url}/{instance.post.author.profile.id}/posts/{instance.post.title}/mpi_{filename}"
