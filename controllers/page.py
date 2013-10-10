# -*- coding:utf-8 -*-
import math
import web

class Page:
    # 当前页面
    page = 0
    # 总页数
    page_count = 0
    # 每页显示的条数
    page_size = 10
    # 记录条数偏移量
    offset = 0
    # 绑定的url
    url = ''
    # 显示的页码数
    shown_count = 7

    def __init__(self, url, inputs, count, page_size=10):
        if 'page' in inputs:
            self.page = int(inputs.page)
        else:
            self.page = 0

        self.url = url
        self.count = count
        self.page_size = page_size
        self.page_count = int(math.ceil(count * 1.0 / self.page_size))
        self.offset = self.page * self.page_size

    def setPageSize(self, page_size):
        self.page = 0
        self.page_size = page_size
        self.page_count = int(math.ceil(self.count * 1.0 / self.page_size))
        self.offset = self.page * self.page_size
    
    def getPageHTML(self):
        if self.page_count <= 0:
            return

        base = '<a href="%spage=%d" class="%s">%s</a>'
        html = base % (self.url, 0, 'other_page_number', '首页'.decode('utf-8'))
        if self.page > 0:
            html += base % (self.url, self.page - 1, 'other_page_number', '上一页'.decode('utf-8'))
        else:
            html += base % (self.url, self.page, 'other_page_number', '上一页'.decode('utf-8'))

        for i in self.getPageRange():
            if i == self.page:
                html += base % (self.url, i, 'current_page_number', str(i+1))
            else:
                html += base % (self.url, i, 'page_number', str(i+1))

        if self.page < self.page_count - 1:
            html += base % (self.url, self.page + 1, 'other_page_number', '下一页'.decode('utf-8'))
        else:
            html += base % (self.url, self.page, 'other_page_number', '下一页'.decode('utf-8'))

        html += base % (self.url, self.page_count - 1, 'other_page_number', '末页'.decode('utf-8'))

        return html
        
    def setShownCount(self, shown_count):
        self.shown_count = shown_count

    def getPageRange(self):
        left = self.page
        right = self.page
        current_count = 0
        
        if self.page_count <= 0:
            return
        while True:
            if right + 1 <= self.page_count:
                right += 1
                current_count += 1
                if current_count == self.shown_count or current_count == self.page_count:
                    return range(left, right)
            if left - 1 >= 0:
                left -= 1
                current_count += 1
                if current_count == self.shown_count or current_count == self.page_count:
                    return range(left, right)
    
