# --*-- encoding: utf-8 --*--

import argparse
import sys
import os
import re
from bs4 import BeautifulSoup
import requests

URL='http://met-art-faces.com/met-art-mirayn-a-cromie/'
URL1='http://met-art-faces.com/met-art-roberta-berti-sebara/'

def download(imgURL, out, title):
    #out = url.split('/')[-1]
    resp = requests.get(imgURL, stream=True)
    if resp.status_code != requests.codes.ok:
        return False

    total = resp.headers.get('content-length')
    if total is None:
        total = 0
    else:
        total = int(total)

    def show_progress(total, acc):
        if total == 0:
            sys.stdout.write("{} ?\r".format(out))
        else:
            #sys.stdout.write("{} [ {:3d}% ]\r".format(100*acc/total, out))
            sys.stdout.write("{} \"{}\" {:3}%\r".format(title, out, int(100*acc/total)))
        sys.stdout.flush()

    acc = 0
    show_progress(total, acc)
    with open(out, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
                acc += len(chunk)
                show_progress(total, acc)
    sys.stdout.write("\n")

    return True

def fetch(from_url, offset, count):
#    with open(from_url, "r") as f:
#        html = f.read()
    
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    html = requests.get(from_url, headers=headers).content
    soup = BeautifulSoup(html)

    # get title
    content = soup.find_all("h2", class_="first")
    if len(content) == 0:
        print("title not found!")
        return
    elif len(content) != 1:
        print("title not unique!")

    #fdir = content[0].contents[0].encode("utf-8").strip().replace("–", "-")
	# create dir
    fdir = content[0].contents[0].strip().replace("–", "-")
    if not os.path.exists(fdir):
        os.mkdir(fdir)
        print("mkdir: \"{}\"".format(fdir))

    # get image url,use 正则表达式
    content = soup.find_all("div", id=re.compile("^post-"))
    if len(content) == 0:
        print("target not found!")
        return
    elif len(content) != 1:
        print("target not unique!")

    imgs = content[0].find_all("img")
    start = 0 if offset is None else offset
    end = len(imgs) if count is None else (start+count)
    print("# of image: {}\n".format(imgs))

    for idx in range(start, end):
        img = imgs[idx]
        url = str(img.attrs["src"])
        url = url.replace("http://t", "http://i")
        ext = url[url.rfind("."):]
        out = "{0}/{1}{2}".format(fdir, idx+1, ext)

        # get image file
        for retry in range(0, 5):
            title = ("({{:{}d}}/{{}})".format(len(str(end))).format(idx+1, end))
            if download(url, out, title):
                break
            print("failed, try again ({})".format(retry+1))


def main():
    #parser = argparse.ArgumentParser(description='nah')
    #parser.add_argument('urls', type=str, nargs="+", help='Specify URLs')
    #parser.add_argument('--offset', type=int, nargs="?", help='offset')
    #parser.add_argument('--count', type=int, nargs="?", help='count')
    #args = parser.parse_args()
    
    #for url in args.urls:
        #print(args.offset, args.count)
        #fetch(url, args.offset, args.count)
    fetch(URL1, None, None)

if __name__ == "__main__":
    main()