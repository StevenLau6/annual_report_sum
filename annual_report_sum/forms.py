from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import BaseFormSet, formset_factory

from bootstrap5.widgets import RadioSelectButtonGroup


COMPANY_CHOICES = (("MSFT", "Microsoft"),("AMZN", "Amazon"), )
YEAR_CHOICES = (("2022", "2022"), ("2021", "2021"), ("2020", "2020"), ("2019", "2019"), ("2018", "2018"))#("2016", "2016"), ("2017", "2017"),
FILETYPE_CHOICES = (("10K", "Form 10K"),("10Q", "Form 10Q"))
SUMTYPE_CHOICES = (("ROO", "Results of Operation"),("Liquidity", "Liquidity"))

class ReportForm(forms.Form):
    #select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    company_select = forms.ChoiceField(choices=COMPANY_CHOICES, help_text="Select company name",required=True,label="Select Company")
    year_select = forms.ChoiceField(choices=YEAR_CHOICES, help_text="Select year",required=True,label="Select year")
    reportfiletype = forms.ChoiceField(choices=FILETYPE_CHOICES, help_text="Select report type",required=True,label="Select Report Type")
    #summarytype = forms.ChoiceField(choices=SUMTYPE_CHOICES, help_text="Select summary type.")
    summarytype = forms.ChoiceField(choices=SUMTYPE_CHOICES, widget=forms.RadioSelect,required=True,label="Select Summary Type")

'''
class ReportSummaryForm(forms.Form):
    #select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    company_select = forms.ChoiceField(choices=COMPANY_CHOICES, help_text="Select company CIK",required=True,label="Select Company")
    year_select = forms.ChoiceField(choices=YEAR_CHOICES, help_text="Select year",required=True,label="Select year")
    reportfiletype = forms.ChoiceField(choices=FILETYPE_CHOICES, help_text="Select report type",required=True,label="Select Report Type")
    #summarytype = forms.ChoiceField(choices=SUMTYPE_CHOICES, help_text="Select summary type.")
    summarytype = forms.ChoiceField(choices=SUMTYPE_CHOICES, widget=forms.RadioSelect,required=True,label="Select Summary Type")
'''