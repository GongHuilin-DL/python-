# -*- coding:utf8 -*-
from lib2to3.pytree import Node
import requests
import json
from urllib import parse
import os
import sys
import time


class BaiduImageSpider(object):
    def __init__(self, category):
        self.book = ['医学', '历史', '政治', '数学', '生物', '社会学', '经济学', '英语', '计算机专业']
        self.json_count = 0  # 请求到的json文件数量（一个json文件包含30个图像文件）
        self.category = category
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5179920884740494226&ipn=rj&ct' \
                   '=201326592&is=&fp=result&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={' \
                   '}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={' \
                   '}&rn=30&gsm=1e&1635054081427= '
        # self.directory = r"DataSet\历史\{}"  # 存储目录  这里需要修改为自己希望保存的目录  {}不要丢        
        # 目录自己修改 
        self.directory = "DataSet/%s/{}"%self.category
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
        }

        '''
        https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&
        fmq=1659756791895_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&
        width=&height=&face=0&istype=2&dyTabStr=MCwzLDUsNCwxLDYsMiw4LDcsOQ%3D%3D&
        ie=utf-8&sid=&word=%E8%AE%A1%E7%AE%97%E6%9C%BA%E4%B8%93%E4%B8%9A%E4%B9%A6%E7%B1%8D%E5%B0%81%E9%9D%A2

        https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&
        fmq=1659757054825_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&
        width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=%E8%8B%B1%E8%AF%AD%E4%B9%A6%E7%B1%8D%E5%B0%81%E9%9D%A2
        '''

    # 创建存储文件夹
    def create_directory(self, name):
        self.directory = self.directory.format(name)
        # 如果目录不存在则创建
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += r'\{}'

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        try:
            strhtml = requests.get(url, headers=self.header)  # Get方式获取网页数据
            # 定义response对应的编码为utf-8
            # strhtml.encoding = 'utf-8'
            strhtml.encoding = strhtml.apparent_encoding

            jsonInfo = json.loads(strhtml.text)
            # jsonInfo = jsonInfo.replace('\\', '\\\\')
            print("len(jsonInfo['data']):", len(jsonInfo['data']))

            # for index in range(30):
            for index in range(len(jsonInfo['data'])):
                path = None
                try:
                    path = str(jsonInfo['data'][index]['thumbURL'])
                except KeyError as e:
                    print('没有找到路径')
                    continue
                
                if path!=None:
                    list_image_link.append(path)
                    # list_image_link.append(jsonInfo['data'][index]['thumbURL'])
                
        except requests.exceptions.ConnectTimeout as e:
            print('ConnectTimeout')

        except requests.exceptions.ReadTimeout as e:
            print('ReadTimeout')

        except requests.exceptions.ConnectionError as e:
            print('ConnectionError')

        except Exception as e:
            print('Error happend!', e)

        finally:
            return list_image_link
        

    # 下载图片
    def save_image(self, img_link, filename):
        res = requests.get(img_link, headers=self.header)
        if res.status_code == 404:
            print(f"图片{img_link}下载出错------->")
        with open(filename, "wb") as f:
            f.write(res.content)
            print("存储路径：" + filename)

    # 入口函数
    def run(self):
        # searchName = input("查询内容：")
        # searchName = "历史书籍封面"
        if self.category in self.book:
            searchName = self.category + "书籍封面"
        else:
            searchName = self.category
        searchName_parse = parse.quote(searchName)  # 编码

        self.create_directory(searchName)
        self.downloaded_pic_count = len(os.listdir(self.directory.format('')))
        print('downloaded_pic_count:', self.downloaded_pic_count)

        #pic_number = 0  # 图像数量
        p = self.downloaded_pic_count // 30
        y = self.downloaded_pic_count % 30
        pic_number = p*30
        # for index in range(self.json_count):
        for index in range(p, self.json_count):
            pn = (index+1)*30
            request_url = self.url.format(searchName_parse, searchName_parse, str(pn))
            #print('pn:', pn)
            #print('request_url:', request_url)

            list_image_link = self.get_image_link(request_url)
            print('list_image len:', len(list_image_link))
            for link in list_image_link:
                pic_number += 1
                if self.downloaded_pic_count < pic_number:
                    self.save_image(link, self.directory.format(str(pic_number)+'.jpg'))
                time.sleep(0.2)  # 休眠0.2秒，防止封ip
        print(searchName+"----图像下载完成--------->")


if __name__ == '__main__':
    category = None
    if len(sys.argv) > 1:
        category = sys.argv[1].strip()
    spider = BaiduImageSpider(category)
    spider.json_count = 3000000   # 定义下载10组图像，也就是三百张
    spider.run()

    '''
    python  getDataSet.py 医学
    python  getDataSet.py 历史
    python  getDataSet.py 政治
    python  getDataSet.py 数学
    python  getDataSet.py 生物
    python  getDataSet.py 社会学
    python  getDataSet.py 经济学
    python  getDataSet.py 英语
    python  getDataSet.py 计算机专业
    '''