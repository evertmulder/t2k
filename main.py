from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
import urllib.request
import requests
import math
import os

def main():
    with open("t2k.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        s2 = soup.select("div.yeeditor a")
        k = []
        for t in s2:
            if t.text == 'Audio':
                link=t.attrs['href']
                if(link.startswith("http://")):
                    link = "https://" + link[7:]
                if link not in k:
                    k.append(link)

        print("Found {0}".format(len(k)))
        downloads = []
        for url in k:
            print("Open {0}".format(url))
            with urllib.request.urlopen(url) as f:
                phtml = BeautifulSoup(f.read(), "html.parser")
                s3 = phtml.select_one("source")
                dl="http:"+s3.attrs['src']
                if dl in downloads:
                    print(dl + " already in download queue.")
                else:
                    downloads.append(dl)
                    # titleEl = phtml.select_one("#sp-page-builder div > div > div.sppb-col-sm-9 > div > div.full-width.m-bottom-20 > h2")
                    titleEl = phtml.select_one("span.text-red")
                    titleEl2 = phtml.select("span.light.font-bold")[0]
                    filename = "TOP 2000 - " + titleEl2.text + " - " + titleEl.text + " - " + Path(dl).name
                    filenameTmp = filename + ".download"
                    if os.path.exists(filenameTmp):
                        os.remove(filenameTmp)
                        print("tmp file removed")
                    if os.path.exists(filename):
                        print(filename + " already downloaded")
                    else:
                        # Streaming, so we can iterate over the response.
                        r = requests.get(dl, stream=True)

                        # Total size in bytes.
                        total_size = int(r.headers.get('content-length', 0))
                        block_size = 1024
                        wrote = 0 
                        with open(filenameTmp, 'wb') as f:
                            for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True, desc=filename):
                                wrote = wrote  + len(data)
                                f.write(data)
                        if total_size != 0 and wrote != total_size:
                            print("ERROR, something went wrong")
                        os.rename(filenameTmp, filename)

if __name__ == "__main__":
    main()
