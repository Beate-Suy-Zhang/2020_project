# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# noinspection PyUnresolvedReferences
import requests
# noinspection PyUnresolvedReferences
import re
# noinspection PyUnresolvedReferences
from requests.exceptions import RequestException
import time
# noinspection PyUnresolvedReferences
from bs4 import BeautifulSoup
# noinspection PyUnresolvedReferences
from selenium import webdriver
import csv
from collections import OrderedDict

# 得加一个用户代理，不然爬不了
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}

# 要爬取的网站————豆瓣top250
url = "https://movie.douban.com/top250"
# 将要爬下来的数据列
num = ['电影名',
       '评分',
       '上映地区',
       '上映时间',
       '导演',
       '编剧',
       '主演',
       '类型',
       '评价人数',
       '五星比例',
       '四星比例',
       '三星比例',
       '二星比例',
       '一星比例']
# 用selenium来爬取网页信息
# 用webdriver打开豆瓣250界面
wd = webdriver.Chrome()
wd.get(url)
# 用“wd2”打开其子界面
wd2 = webdriver.Chrome()


# 存放文本信息
def save(lst):
    with open(r'C:\Users\Beate\Desktop\data1.txt', 'a')as file:
        for dic in lst:
            for key, value in dic.items():
                file.write(key+':'+str(value)+'    ')
            file.write('\n')
    # test = pandas.DataFrame(columns=num, data=lst)
    # test.to_csv('D:/test.csv')
    print('save:文件已保存')


# 将爬下来的数据保存到表格中
def save_csv(lst):
    with open('D:/test.csv1', 'a', newline='', encoding='utf-8') as file:
        wtr = csv.writer(file)
        # 一次写一行
        for data in lst:
            wtr.writerow(data)
    print('save_csv:文件已保存')


def get_data():
    # 豆瓣top250网页一共10页，每页有25个电影
    for i in range(10):
        # 找到页面的每一个电影
        div_list = wd.find_elements_by_css_selector('div.info')

        # 用于存入.txt的list
        data = []
        # 用于存入.csv的list
        data_csv = []
        # 对于每一部电影里找：
        for div in div_list:
            # 用于存入.txt的dictionary
            dic = {}
            # 用于存入.csv的list
            temp = []

            # 电影名（分别存入字典和列表）
            dic['电影名'] = div.find_element_by_css_selector('span.title').text
            temp.append(div.find_element_by_css_selector('span.title').text)

            # 评分
            dic['评分'] = div.find_element_by_css_selector('span.rating_num').text
            temp.append(div.find_element_by_css_selector('span.rating_num').text)

            # “wd2”获取电影的子页面，然后在子页面继续爬取数据
            target = div.find_element_by_xpath('div[@class="hd"]/a').get_attribute('href')
            wd2.get(target)

            # 上映地区（借用"https://www.cnblogs.com/cxxBoo/p/12531454.html"的代码）
            html = requests.get(target, headers=headers)
            bs = BeautifulSoup(html.text, 'lxml')
            dic['上映地区'] = bs.find(id="info").find(text='制片国家/地区:').next_element.lstrip().rstrip()
            temp.append(bs.find(id="info").find(text='制片国家/地区:').next_element.lstrip().rstrip())

            # 上映时间
            time_place = wd2.find_element_by_xpath('//span[@property="v:initialReleaseDate"]')
            dic['上映时间'] = time_place.text[0:10]
            temp.append(time_place.text[0:10])

            # 导演，编剧，主演
            spans = wd2.find_elements_by_css_selector('span.attrs')
            j = 4
            for span in spans:
                dic[num[j]] = span.text
                temp.append(span.text)
                j = j+1

            # 类型
            types = wd2.find_elements_by_xpath('//span[@property="v:genre"]')
            types_con = ''
            for type1 in types:
                types_con = types_con+'/'+type1.text
            dic['类型'] = types_con
            temp.append(types_con)

            # 评价人数
            dic['评价人数'] = wd2.find_element_by_xpath('//span[@property="v:votes"]').text
            temp.append(wd2.find_element_by_xpath('//span[@property="v:votes"]').text)

            # 一~五星评价比例
            rates = wd2.find_elements_by_css_selector('span.rating_per')
            j = 9
            for rate in rates:
                dic[num[j]] = rate.text
                temp.append(rate.text)
                j = j+1

            # 保存这个电影的数据
            data.append(dic)
            data_csv.append(temp)
            time.sleep(3)
        # 保存这一页电影的数据
        save(data)
        save_csv(data_csv)
        # 模仿浏览时点击“后页”
        if i != 9:
            wd.find_element_by_link_text('后页>').click()
        print('第'+str(i+1)+'页数据已获取')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 首先存入列表每一列数据的名称
    with open('D:/test.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(num)
    #  获取数据
    get_data()
    # 关闭页面
    wd2.quit()
    wd.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
