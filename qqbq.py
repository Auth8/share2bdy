# -*- coding:utf-8 -*-
# 抓取qq表情图片
import urllib
import urllib2
import re
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')


class Spider:
    MAX_PAGE = 1
    FILE_SAVE_BASE_PATH = "./qqbq/"
    LOG_FILE_PATH = "./runtime.log"

    def __init__(self):
        self.siteURL = 'http://qq.yh31.com/zjbq/'

    def getPage(self, pageIndex):
        url = self.siteURL + "List_" + str(pageIndex) + ".html"
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf8')

    def getUrlContent(self, url):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        return response.read()

    def getContents(self, pageIndex=''):
        if pageIndex == '':
            pageIndex = 1
        page = self.getPage(pageIndex)
        # pattern = re.compile('<a href=\"(.*?)\"><img class=\"pic2\"', re.S)
        items = re.findall('<a href="([\d\w\/\.]*?)"><img class="pic2"', page)
        for item in items:
            # print item
            itemurl = "http://qq.yh31.com" + item
            pageContent = self.getUrlContent(itemurl)
            # pageContent = pageContent.decode('utf8')
            # 获取表情标题
            title = re.findall('<div class="c_title_text"\
>([\s\S]*?)<\/div>', pageContent)
            title = title[0].decode('utf8').strip().lstrip().rstrip(',')
            iis = re.findall(u'<img src="\
([\d\w\/\.]*?)" alt="(.*?)"', pageContent)
            self.writeLog(u"共有" + str(len(iis)) + u"张图片\n")
            # 循环表情图片列表
            for img in iis:
                if img[1] == '':
                    file_name = os.path.basename(img[0]).split('.')[0]
                else:
                    file_name = img[1].decode('utf8')
                print img[0], file_name
                self.downGif("http://qq.yh31.com" + img[0], file_name, title)
                # break
        self.writeLog(u"第" + str(pageIndex) + "页处理完成\n")
        if pageIndex < self.MAX_PAGE:
            self.getContents(pageIndex+1)
            pass

    def downGif(self, url, name, path):
        save_path = self.FILE_SAVE_BASE_PATH + path
        if os.path.exists(self.FILE_SAVE_BASE_PATH) == False:
            os.mkdir(self.FILE_SAVE_BASE_PATH)
        if os.path.exists(save_path) == False:
            os.mkdir(save_path)
        # 下载图片
        save_path_name = save_path + "/" + name + os.path.splitext(url)[1]
        # print save_path_name
        self.writeLog(save_path_name + u"下载完成\n")
        urllib.urlretrieve(url, save_path_name)

    def writeLog(self, content):
        file_obj = open(self.LOG_FILE_PATH, 'a')
        file_obj.writelines(content)
        file_obj.close()
        pass

spider = Spider()
spider.getContents()
