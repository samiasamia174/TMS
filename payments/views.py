# payments/views.py
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from buses.models import Bus
from .models import Payment
import uuid
