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
    return F"{pre_url}/{instance.profile.username}/bio/ab{date}{filename}"


def AuthorImage(instance, filename):
    return F"{pre_url}/{instance.profile.username}/bio/ai{date}{filename}"


def PostBanner(instance, filename):
    return F"{pre_url}/{instance.author.profile.username}/posts/{instance.title}/pb{filename}"


def PostImage(instance, filename):
    return F"{pre_url}/{instance.author.profile.username}/posts/{instance.title}/pi{filename}"


def MorePostImage(instance, filename):
    return F"{pre_url}/{instance.post.author.profile.username}/posts/{instance.post.title}/mpi{filename}"
