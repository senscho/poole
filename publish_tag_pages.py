template = r"""
---
layout: page
title: "Tag: {{}}"
---

[see all Tags]({{site.url}}{{site.baseurl}}/tags/)
{% include posts_by_tag.html tag="{{}}" %}
""".strip()

import subprocess
import os

subprocess.call( 'rm -rf tags'.split(' '))
subprocess.call( 'mkdir tags'.split(' '))

# tags = ['one','two','three']

tag_file = './_site/tags/index.html'

with open(tag_file,'r') as fp:
    whole = fp.read()

section = whole.split('class="tagcloud">')[1].split('</ul>')[0]
tags = [x.split('</a>')[0].split('>')[1] for x in section.split('<a')][1:]
print tags
for tag in tags:
    with open('./tags/{}.md'.format(tag),'w') as fp:
        fp.write( template.replace('{{}}',tag) )