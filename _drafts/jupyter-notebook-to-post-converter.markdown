---
title: Jupyter Notebook to Post Converter
layout: post
---

{% highlight python %}
#!/usr/local/bin/python

'''
Jupyter Publish Tool
'''

file_name = 'Jupyter-Blogging-Demo'
ipnb_path = './_ipynbs'
post_path = './_posts'

import sys
try:
    file_name = sys.argv[1]
except:
    pass

assert file_name

import datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

in_name = '{}.ipynb'.format(file_name)
out_name = '{}-{}.markdown'.format(today, file_name)

import subprocess
cmd = 'jupyter nbconvert {}/{} --to html --template basic --stdout'.format(ipnb_path,in_name)
content = subprocess.check_output(cmd.split(' '))

lines = [line.strip() for line in content.split('\n')]
if lines[0] != '---':
    addline = []
    addline.append('---')
    addline.append('title: {}'.format(file_name.replace('-',' ')))
    addline.append('layout: post')
    addline.append('use_math: true')
    addline.append('hide_code: false')
    addline.append('---')
    lines = addline + lines

import os
with open( os.path.join(post_path,out_name), 'w' ) as fp:
     fp.write('\n'.join(lines))
{% endhighlight %}
