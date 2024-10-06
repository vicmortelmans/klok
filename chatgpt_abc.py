#!/usr/bin/env python
from dotenv import load_dotenv
import json
import logging
from openai import OpenAI
import os
import re
from sys import stdout

logger = logging.getLogger("chatgpt_abc")
handler = logging.StreamHandler(stdout)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d %(funcName)s] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

load_dotenv(os.getenv('HOME') + "/.env")  # contains OPENAI_API_KEY
AI = OpenAI()

def abc():
    with open('chatgpt_prompt_composer.json') as f:
        messages = json.load(f)
    messages.append({"role": "user", "content": "That sounds great! Make another one!"})
    completion = AI.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    response = completion.choices[0].message.content
    return response

def extract_code_block(markdown_string):
    # Regex to find code blocks marked by ```
    code_block_pattern = re.compile(r'```.*?\n(.*?)```', re.DOTALL)
    
    # Find all code blocks in the markdown string
    code_block = code_block_pattern.search(markdown_string).group(1)
    
    return code_block

print(extract_code_block(abc()))
