GMolescan

## 0x01 介绍
GMolescan 是一款基于flask分布式扫描器,从服务器下载未扫描完成的插件在节点执行扫描任务,扫描结果post提交到数据库中，同时telegram通知。

## 0x02 原理

基于flask api+mysql 服务自动化下载插件，执行扫描，推送结果功能。


## 0x03 技术细节

agent 从接口获取未扫描完成的插件名并且下载插件到本地，扫描成功存在漏洞的结果post发送给接口。
服务器接口写入数据库并且telegram通知。
当前插件扫描完成时，再遍历漏洞插件未扫描完成的插件名。删除当前扫描完成的插件脚本并且从服务器上下载新的插件脚本继续自动化执行任务。
```python
插件名变量
r = requests.get('http://8.211.187.204:9090/initplugin', timeout=5)
    print(r.content)
    print(type(r.content))
    cvenames = ast.literal_eval(r.content.decode('utf-8'))
    exploitname = cvenames[0]

```

```python
下载后自动注册插件

def download(pluginname):
    store_path = 'C:\\Users\\exp\\Desktop\\exploitscan\\plugin'
    url = 'http://8.211.187.204:9090/download?file=' + pluginname + '.py'
    filepath = os.path.join(store_path, 'exploit.py')
    file_data = requests.get(url, headers=headers, allow_redirects=True).content
    with open(filepath, 'wb') as handler:
        handler.write(file_data)
    '''
    
    '''

```

```python
上传扫描结果
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

```

## 0x04 展望

	1.丰富更多插件
	2.针对爆破，反弹，回显等单独做出模块
	3.后台可以下发指令让多节点执行不同的扫描任务