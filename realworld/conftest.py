import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realworld.settings')
sys.path.append(os.path.dirname(__file__))
django.setup()