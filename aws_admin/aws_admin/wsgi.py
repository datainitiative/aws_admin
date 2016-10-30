"""
WSGI config for aws_admin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/django-apps/aws_admin/aws_admin/')
# Use this for single Django site in a single mod_wsgi process
#os.environ.setdefault("PYTHON_EGG_CACHE", "/django-apps/aws_admin/aws_admin/egg_cache")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aws_admin.settings")
# Use this for multiple Django site in a single mod_wsgi process
os.environ["PYTHON_EGG_CACHE"] = "/django-apps/aws_admin/aws_admin/egg_cache"
os.environ["DJANGO_SETTINGS_MODULE"] = "aws_admin.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()