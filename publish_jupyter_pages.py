#!/usr/local/bin/python

'''
Jupyter Publish Tool
'''


file_name = 'Jupyter-Blogging-Demo'
ipnb_path = './_ipynbs'
post_path = './_posts'

defaults = {}
defaults['layout'] = 'post'
defaults['use_math'] = 'true'
defaults['hide_code'] = 'false'
defaults['remove_source'] = 'false'

def read_front_matter(content):
    bOpen = False
    for line in content.split('\n'):
        if line[0:3] == '---':
            if bOpen: break
            else: bOpen = True

        if bOpen:
            params = line.strip().split(':')
            param = params[0]
            value = ':',join(params[1:])
            defaults[param] = value


def make_valid_filename(fname):
    tokens=' /<>:"/\\|?*.!='
    for token in tokens:
        fname = fname.replace(token,'-')

    while '--' in fname:
        fname = fname.replace('--','-')

    if fname[-1]=='-':
        fname = fname[:-1]

    return fname

import sys
try:
    file_name = sys.argv[1]
    new_title = sys.argv[2]
except:
    pass

assert file_name

import datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

try:
    new_title
    new_title_file = make_valid_filename(new_title)
except:
    new_title = file_name
    new_title_file = make_valid_filename(file_name)

in_name = '{}.ipynb'.format(file_name)
out_name = '{}-{}.markdown'.format(today, new_title_file)

import subprocess
cmd = 'jupyter nbconvert {}/{} --to html --template basic --stdout'.format(ipnb_path,in_name)
content = subprocess.check_output(cmd.split(' '))

lines = [line.strip() for line in content.split('\n')]
if lines[0] != '---':
    addline = []
    addline.append('---')
    addline.append('title: {}'.format(new_title))
    addline.append('layout: post')
    addline.append('use_math: true')
    addline.append('hide_code: false')
    addline.append('---')
    lines = addline + lines


import os
with open( os.path.join(post_path,out_name), 'w' ) as fp:
    fp.write('\n'.join(lines))

cmd = 'mv {}/{}.ipynb {}/{}.ipynb'.format(ipnb_path,file_name,ipnb_path,new_title_file)
subprocess.check_output(cmd.split(' '))