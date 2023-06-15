#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2023/06/15 19:29:51
@Author  :   Shuaiqi 
@Version :   1.0
@Contact :   shuaiqizju@gmail.com
@Desc    :   None
'''

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ReportForm#ContactForm, ContactFormSet, FilesForm, , ReportSummaryForm
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import os
import json
import requests
import pandas as pd
import numpy as np

#import traceback
#from personality_chatbot.response_gen import emotional_response_gen
#from .response_gen import emotional_response_gen

#from transformers import BertTokenizer, BertConfig, BertForSequenceClassification
#from transformers import AdamW, get_linear_schedule_with_warmup
#from transformers import AutoTokenizer


#import torch
#from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer, PegasusTokenizer
#from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments
#from transformers import LEDTokenizer, LEDForConditionalGeneration, Trainer, TrainingArguments
#from datasets import load_dataset
#from .text_summarizer import Text_Summarizer

import pdb

#INPUT_MAX_LENGTH=8192
#OUTPUT_MAX_LEN=400
#OUTPUT_MIN_LEN=300



INPUT_CSV_PATH="D:\\code\\ml\\Findsum\\web_demo\\annual_report_sum\\annual_report_sum\\static\\csv\\"
#"/home/shuaiqi/develope/web/FINDSum/web_demo/annual_report_sum/static/csv/"

class FormReportView(FormView):
    template_name = "app/form_10kreport.html"
    form_class = ReportForm


def get_report_summary(config_dict):
    generated_summary = ''
    report_file_url = ''
    company_cik = config_dict['company_cik']
    report_year = config_dict['report_year']
    report_file_type = config_dict['report_file_type']
    report_summary_type = config_dict['report_summary_type']
    input_csv_file_path = INPUT_CSV_PATH + "findsum_demo_data.csv"
    input_pd = pd.read_csv(input_csv_file_path, sep=',')
    
    #pdb.set_trace()
    select_pd = input_pd[(input_pd['company']==company_cik) & (input_pd['year']==int(report_year)) & (input_pd['report_type']==report_file_type)]
    report_file_url = select_pd['report_url'].values[0]
    if report_summary_type=="ROO":
        generated_summary = select_pd['roo_summary'].values[0]
    elif report_summary_type=="Liquidity":
        generated_summary = select_pd['liquidity_summary'].values[0]
    
    return generated_summary,report_file_url


@csrf_exempt
def annual_report_select(request):
    #pdb.set_trace()
    if request.method == 'POST':
        company_cik = request.POST.get('company_select')
        report_year = request.POST.get('year_select')
        report_file_type = request.POST.get('reportfiletype')
        report_summary_type = request.POST.get('summarytype')
        config_dict = {}
        config_dict['company_cik'] = company_cik
        config_dict['report_year'] = report_year
        config_dict['report_file_type'] = report_file_type
        config_dict['report_summary_type'] = report_summary_type
        generated_summary,report_file_url = get_report_summary(config_dict)
        #generated_summary = "WTF!"
        #pdb.set_trace()
        #form = ReportSummaryForm()
        #context = {'form': form}
        context = {'company_cik':company_cik,'report_year':report_year,'report_file_type':report_file_type,'report_summary_type':report_summary_type,'report_file_url':report_file_url,'generated_summary': generated_summary}
        template_name = "app/form_10kreportsummary.html"
        return render(request, template_name, context)
    if request.method == 'GET':
        form = ReportForm()
        context = {'form': form}
        template_name = "app/form_10kreport.html"
        return render(request, template_name, context)

@csrf_exempt
def system_about_page(request):
    template_name = "app/form_10kreport_about.html"
    return render(request, template_name)

@csrf_exempt
def system_features_page(request):
    template_name = "app/form_10kreport_features.html"
    return render(request, template_name)

#@csrf_exempt
#def get_report_doc(request):
#    #if request.method == 'POST':
#    pdb.set_trace()
#    response_dict = {}
#    #response_dict["input_str"] = input_str
#    #print()
#    response_json = json.dumps(response_dict)
#
#    return HttpResponse(response_json)





'''
MODEL_PATH_DICT={}
MODEL_PATH_DICT['led_sum']={}
MODEL_PATH_DICT['led_sum']['liquidity_1']="/home/disk1/data/shuaiqi/sec-edgar/model/transformers411/LED_base/liquidity_8000_300/input_8_1000_300_without_seg_18_1/checkpoint-10300"

#LED_MODEL_CP_PATH = "/home/disk1/data/shuaiqi/sec-edgar/model/transformers411/LED_base/liquidity_8000_300/input_8_1000_300_without_seg_18_1/checkpoint-10300"
#led_sum_tokenizer = AutoTokenizer.from_pretrained(LED_MODEL_CP_PATH) 
#led_sum_model = LEDForConditionalGeneration.from_pretrained(LED_MODEL_CP_PATH).to(torch_device)

#def LEDSUMInference(input_seq,led_sum_tokenizer,led_sum_model):
def LEDSUMInference(input_seq,summarizer_dict,summarizer_name='led_sum',input_sum_type='liquidity'):
    #inputs = led_sum_tokenizer(input_seq, return_tensors = "pt")
    #outputs = led_sum_model(**inputs)
    output_summary = ""

    #inputs = tokenizer(test_batch,truncation=True, padding=True, max_length=input_max_length, return_tensors='pt').to(torch_device)
    #predictions = model.generate(**inputs,max_length=400,min_length=300,num_beams=5,length_penalty=2.0,no_repeat_ngram_size=3)
    #predictions = tokenizer.batch_decode(predictions)
    Summarizer = Text_Summarizer(summarizer_dict,'liquidity_1',summarizer_name)
    summary_seg_1_text = Summarizer.summarize(input_seq, output_len=300, input_max_length = 8192)
    output_summary = summary_seg_1_text
    
    #pdb.set_trace()
    return output_summary
    

def prepare_input_seq(input_file_path,input_cik,input_year,input_sum_type):
    input_text = ""
    if input_sum_type="Liquidity":
        pass
    elif input_sum_type="ROO":
        pass
    return input_text


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''


