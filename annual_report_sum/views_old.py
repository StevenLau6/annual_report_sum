#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2022/08/21 11:13:20
@Author  :   sq 
@Version :   1.0
@Desc    :   None
'''

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import os
import json
import requests
import time
import pandas as pd
import numpy as np

#import traceback
#from personality_chatbot.response_gen import emotional_response_gen
#from .response_gen import emotional_response_gen

#from transformers import BertTokenizer, BertConfig, BertForSequenceClassification
#from transformers import AdamW, get_linear_schedule_with_warmup
#from transformers import AutoTokenizer


import torch
#from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer, PegasusTokenizer
#from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments
from transformers import LEDTokenizer, LEDForConditionalGeneration, Trainer, TrainingArguments
#from datasets import load_dataset
from .text_summarizer import Text_Summarizer

import pdb

INPUT_MAX_LENGTH=8192
OUTPUT_MAX_LEN=400
OUTPUT_MIN_LEN=300



INPUT_CSV_PATH="/home/shuaiqi/develope/web/FINDSum/web_demo/annual_report_sum/static/csv/"

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



@csrf_exempt
def get_response(request):

    input_cik = request.POST.get('cik')
    input_year = request.POST.get('year')
    #input_report_type = request.POST.get('report_type')
    input_sum_type = request.POST.get('sum_type')

    # response generation
    #generator_dict={}
    #generator_dict['model_name']='t5_base_PELD'
    #generator_dict['model_path']="/home/disk1/data/shuaiqi/emo_response_gen/model/t5_base/PELD/checkpoint-3906"

    input_str = prepare_input_seq(INPUT_CSV_PATH,input_cik,input_year,input_sum_type)

    output_summary = LEDSUMInference(input_str,summarizer_dict,summarizer_name='led_sum',input_sum_type='liquidity')


    response_dict = {}
    response_dict["input_str"] = input_str
    response_dict["summary"] = output_summary
    #print()
    response_json = json.dumps(response_dict)

    return HttpResponse(response_json)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
