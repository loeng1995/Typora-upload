import re
import sys,os
import mimetypes

import requests

from time import sleep


############      参数配置   ###############
CACHE = False

# ↓↓↓↓↓  此处的 E 为电脑盘符. 更改为你电脑除 C盘以外的硬盘. 此`盘符`作用于python读取并临时创建图片文件,成功后即删除
PATH= 'E'                                               

# ↓↓↓↓↓  送请求所携带的cookie  浏览器F12.->network ->抓包即可获得.
TOKEN = '56|F1P2pVbfADCEtJjlQT1VEg5XiOqTIpBfP4xjZXNj'  

# ↓↓↓↓↓  #此处填写上传图片的url
URL = 'https://替换图床地址'            

#  headers设置
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Authorization': TOKEN,
    'Accept': 'application/json',
    'authorization': '替换为你的authorization',    #替换为你的authorization
    'Referer': f'{URL}'
}

##############################################


## 上传
def upload_img(file,file_name,file_type,**kwargs):
    global URL
    url = f'{URL}/rest/upload'
    resp = requests.post(
        url,
        files={
            "files":(
                file_name,
                file,
                file_type
                )
            
            },
        headers=headers,
        verify=False,
        **kwargs
        )
    resp.close()
    
    if resp.status_code == 200:
        return resp.json()
    else:
        return 'Net Error!!'
    
def get_sys_arg():
    paths = sys.argv[1:] #获取cmd传入的参数,因为第一个是要执行的py程序,第二个及以后才是图片的绝对路径
    return paths

def parse(t):
    '''
    解析路径是网络地址还是本地地址

    返回文件没有关闭, 则必须关闭.
    '''
    query = re.compile(r'http[s]://')
    if query.match(t):
        ext = mimetypes.guess_extension(mimetypes.guess_type(t))
        with open(f'{PATH}:/tmp.{ext}','wb') as f:
            
            resp = requests.get(t,verify=False)
            f.write(resp.content)
            f.close()
            global CACHE
            CACHE = True
            return f'{PATH}:/tmp.{ext}'
    else:
        return t
    
def parse_url(json):
    url = json['data'][0]['url']
    newUrl = f'{URL}{url}' #.replace('\\','') ##url地址

    return newUrl

def clear_tmp():
    global CACHE
    if CACHE:
        os.remove(f'{PATH}:/tmp.jpg')
    CACHE = False    
    return

def get_file_name(t:str):
    name = t.split(r'\\')[-1]
    return name

if __name__ == '__main__':
    command = get_sys_arg()
    if command:
        for item in command:
            #print('yunxing ')

            with open(parse(item),'rb') as img: 
                #print(item)
                file_type = mimetypes.guess_type(item)[0]
                file_name = get_file_name(item)
                #print("文件名",file_name,file_type)
                js = upload_img(img,file_name,file_type)
                print(parse_url(js))
                sleep(1)
                
                img.close()
                clear_tmp()
        
    else:
        img = open('E:/test.png','rb')
        file_type = mimetypes.guess_type("E:/test.png")[0]
        print(file_type)
        js = upload_img(img,'hh.png',file_type=file_type)
        print(js)
        img.close()
   