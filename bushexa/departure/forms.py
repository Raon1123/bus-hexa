from django import forms

import datetime

from .helper.select_list_builder import *


class TimeForm(forms.Form):
    hour = forms.CharField(label='', required=False, 
        widget=forms.Select(choices=build_hour_select_list()))
    minute = forms.CharField(label=': ', label_suffix='', required=False, 
        widget=forms.Select(choices=build_minute_select_list()))
