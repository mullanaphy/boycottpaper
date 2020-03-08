# -*- coding: utf-8 -*-
"""
Boycott Paper

LICENSE

This source file is subject to the Open Software License (OSL 3.0)
that is bundled with this package in the file LICENSE.txt.
It is also available through the world-wide-web at this URL:
http://opensource.org/licenses/osl-3.0.php
If you did not receive a copy of the license and are unable to
obtain it through the world-wide-web, please send an email
to hi@john.mu so we can send you a copy immediately.

@copyright Copyright (c) 2014 John Mullanaphy (https://john.mu/)
@license http://opensource.org/licenses/osl-3.0.php  Open Software License (OSL 3.0)
@author John Mullanaphy <hi@john.mu>
"""

from comic.models import Comic, Panel, Hidden, Commentary
from django.contrib import admin


# Can't forget to register our Comic and Panel models. Comic is the meta data
# corresponding to a comic while Panel is the individual frames. I did it this
# way in case I wanted to make it easier to display 4 panel comics on web and
# mobile by having them reflow (web would be 4x1, mobile 1x4).
admin.site.register(Comic)
admin.site.register(Panel)
admin.site.register(Hidden)
admin.site.register(Commentary)
