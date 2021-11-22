#!/usr/bin/env python
import os
import sys

sys.path.append("..")

from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "test_app.settings"

import django

django.setup()

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
