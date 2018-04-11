#!/usr/local/bin/python

'''
Jupyter Publish Tool
'''

import sys
import os


if __name__ == '__main__':
    file_name = './_ipynbs/Euler Number'
    post_path = './_posts'
else:
    bexit = False
    if len(sys.argv) > 1:
        file_name = sys.argv[0]
    else:
        print('Please provide input file name')
        bexit = True

    if len(sys.argv) > 2:
        post_path = sys.argv[1]
    else:
        print('Please provide output directory name')
        bexit = True
    if bexit:
        exit()

def find_file(file_name, try_ext):
    # repect the input file name.
    if not os.path.isfile(file_name):
        # print('File not found at: ' + file_name)
        _, ext = os.path.splitext(file_name)
        if ext != try_ext:
            # if not found try with given extension
            file_name += '.ipynb'
            # print('Trying with: ' + file_name)
            if not os.path.isfile(file_name):
                # print('File not found at: ' + file_name)
                return False
        else: return False
    return file_name

def read_front_matter(content):
    bOpen = False
    ret = {}
    for line in content.split('\n'):
        if line.strip()[0:3] == '---':
            if bOpen: break
            else:
                bOpen = True
        elif bOpen:
            params = line.strip().split(':')
            param = params[0]
            value = ':'.join(params[1:])
            ret[param] = value
    return ret

def replace_front_matter(content,fm):
    bOpen = False

    iClosed = -1
    lines = content.split('\n')
    for i,line in enumerate(lines):
        if line[0:3].strip() == '---':
            if bOpen:
                iClosed = i
                break
            else:
                bOpen = True
                iOpen = i

    if iClosed == -1:
        print('front matter is not correct in current ipynb file')
        exit()
    
    fm_lines = []
    for key,value in fm.iteritems():
        fm_lines.append('{}: {}'.format(key,value))

    ret_lines = lines[:iOpen+1] + fm_lines + lines[iClosed:]
    return '\n'.join(ret_lines)

def add_default_to_front_matter(front_matter, defaults):
    front_keys = front_matter.keys()
    for key,value in defaults.iteritems():
        if key in front_keys:
            continue
        front_matter[key] = value

    return front_matter.keys()
def make_valid_filename(fname):
    # tokens=' /<>:"/\\|?*.!='
    # for token in tokens:
    #     fname = fname.replace(token,'-')

    # str is immutable. convert into list
    fname = list(fname)
    for i,character in enumerate(fname):
        if not character.isalnum():
            if character not in ['_']:
                fname[i] = '-'
    # back to str
    fname = ''.join(fname)
    while '--' in fname:
        fname = fname.replace('--','-')
    if fname[-1]=='-':
        fname = fname[:-1]
    if fname[0]=='-':
        fname = fname[1:]    
    return fname

def get_tag(content, start_i):
    start_i = content.find('<',start_i)
    tag_i = content.find(' ',start_i+1)
    end_i = content.find('>',start_i + 1)

    if tag_i > end_i: tag_i = end_i -1

    if start_i == -1 or end_i == -1:
        return -1,''

    tag = content[start_i+1:tag_i+1].strip()
    return end_i,tag
    
def remove_tag(content, search_list):
    # tag to be removed
    _, tag_remove = get_tag(search_list[-1],0)

    search_depth = 0
    pre = ''
    rest = content

    # progress with search tree
    search_i = -1
    for search in search_list:
        search_i = content.find(search, search_i+1)

        if search_i == -1:
            print('no matching')
            return False, content
        search_i += len(search)

    # now find tag range
    tag_start = search_i - len(search)
    tag_depth = 1   # we already found the tag to delte
    search_i -= 1

    while search_i != -1 and tag_depth>0:
        search_i, tag = get_tag(content, search_i+1)
        # print tag
        if tag == tag_remove:
            tag_depth += 1
            # print search_i, tag, tag_depth
        if tag == '/'+tag_remove:
            tag_depth -= 1
            # print search_i, tag, tag_depth

    if search_i == -1:
        print('cannot find the tag range')
        return False, content

    tag_end = search_i
    # tag_section = content[tag_start:tag_end+1]
    # print tag_section
    return True, content[:tag_start] + content[tag_end+1:]

    
# print(make_valid_filename('!a!bc?!def/_new-old-'))

ret = find_file(file_name,'.ipynb')
if not ret:
    print('Cannot find File: '+file_name)
    exit()
else:
    file_name = ret

print('Input File: '+file_name)
    

# out_name = '{}-{}.markdown'.format(today, new_title_file)

import subprocess
cmd1 = 'jupyter nbconvert'
cmd2 = '"{}"'.format(file_name)
cmd3 = '--to html --template basic --stdout'

print cmd1+cmd2+cmd3
content = subprocess.check_output(' '.join([cmd1, cmd2, cmd3]),shell=True)
# cmd1.split(' ') + [cmd2] + cmd3.split(' ')
front_matter = read_front_matter(content)

import datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
todaytime = now.strftime('%Y-%m-%d %H:%M:%S')   # %z for timezone in aware object

defaults = {}
defaults['layout'] = 'post'
defaults['use_math'] = 'true'
defaults['hide_code'] = 'false'
defaults['remove_src'] = 'false'
defaults['date'] = todaytime


keys = add_default_to_front_matter(front_matter,defaults)

# Priority: file_title --> title --> file_name
if 'file_title' in keys:
    out_name = make_valid_filename(front_matter['file_title'])
    print('file_title: {}'.format(out_name))
elif 'title' in keys:
    out_name = make_valid_filename(front_matter['title'])
    print('title: {}'.format(out_name))
else:
    out_name = os.path.split(os.path.splitext(file_name)[0])[1]
    out_name = make_valid_filename(out_name)
    print('file_name: {}'.format(out_name))

out_name = '{}-{}.markdown'.format(today, out_name)

search_list1 = [
    '<div class="cell border-box-sizing code_cell rendered">',
    '<div class="input">'
    ]
search_list2 = [
    '<div class="output_area">',
    '<div class="prompt">'
    ]


if front_matter['remove_src']:
    success = True
    while success:
        success, content = remove_tag(content, search_list1)
    success = True
    while success:
        success, content = remove_tag(content, search_list2)


content = replace_front_matter(content, front_matter)


with open('temp.txt','w') as fp:
    fp.write(content)

cmd = 'mv temp.txt {}/{}'.format(post_path,out_name)
subprocess.check_output(cmd.split(' '))