# -*- coding:utf-8 -*-
import web
from code import session
from config.settings import render
from config.settings import forum_render
from config.settings import auth_render
from config.settings import admin_render 
import tools
from models import model
from controllers.page import Page

# 主页
class Index:
    def GET(self):
        #  获取news_info表的前5条技术并用于主页的显示
        return render.index(model.get('news_info', order='news_pub_time desc', limit=5))

# 新闻列表页面
class News:
    def GET(self):
        i = web.input()
        page = Page('/news?', i, model.getcount('news_info'), 20)
        return render.news(
                model.get(
                    'news_info', 
                    order='news_pub_time desc', 
                    limit=page.page_size, 
                    offset=page.offset
                    ), 
                page
                )

# 新闻的详细页面
class NewsDetail:
    def GET(self, id):
        return render.news_detail(
                model.get('news_info', where='news_id=' + id)
                );

# 产品列表
class Product:
    def GET(self):
        i = web.input()
        page = Page('/product?', i, model.getcount('product_info'), 10)
        return render.product(
                            model.get(
                                    'product_info', 
                                    order='product_date', 
                                    limit=page.page_size, 
                                    offset=page.offset
                                    ), 
                            page
                            )

# 登录界面
class Login:
    def GET(self):
        return auth_render.login()

    def POST(self):
        data = web.input(username='', password='')
        if data.username != '' and data.password != '' and tools.check_user(data.username, data.password):
            session.login = True
            session.username = data.username
            raise web.seeother('/')
        raise web.seeother('/message?msg=' + '用户名或密码错误!'.decode('utf-8'))

# 登出处理
class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

# 注册界面
class Register:
    def GET(self):
        return auth_render.register() 

    def POST(self):
        i = web.input(username = '', password1 = '', password2 = '', email = '')
        if i.username != '' and i.password1 != '' and i.password2 != '' and i.email != '' and i.password1 == i.password2:
            model.add(
                    'member_info', 
                    member_username = i.username, 
                    member_password = tools.make_password(i.password1), 
                    member_email = i.email,
                    head_image='/static/images/head_images/default.jpg' 
                    )
            raise web.seeother('/')
        else:
            raise web.seeother('/message?msg=' + '注册信息有误!'.decode('utf-8'))

# 论坛主页
class Forum:
    def GET(self):
        i = web.input(post_type = '', post_class = '')
        page = Page('/forum?', i, model.getcount('forum_posts'), 20)

        query_sql = 'select * from forum_posts as a, post_types as b where a.post_type = b.post_type'\
                    ' order by top desc, essence desc, recommend desc, post_pub_time asc limit $x offset $y'

        if i.post_type != '':
            if i.post_type == '0':
                return forum_render.index(
                                        model.getbysql(
                                                        query_sql,
                                                        vars={'x':page.page_size, 'y':page.offset}
                                                    ),
                                        page
                                        )
            else:
                return forum_render.index(
                                        model.getbysql(
                                                    'select * from forum_posts as a, post_types as b where a.post_type = b.post_type'\
                                                    ' and (a.post_type = $x or top>0) order by top desc, essence desc, recommend desc,'\
                                                    ' post_pub_time asc limit $y offset $z',
                                                    vars={'x':i.post_type, 'y':page.page_size, 'z':page.offset}
                                                    ),
                                        page
                                        )
        else:
            return forum_render.index(
                                    model.getbysql(
                                                    query_sql,
                                                    vars={'x':page.page_size, 'y':page.offset}
                                                ),
                                    page
                                    )

# 主题详细页面
class Topic:
    def GET(self, id):
        i = web.input()
        page = Page('/topic/'+id+'?', i, model.getcount('forum_backposts', where='post_id=' + id), 10)
        model.update('forum_posts', where='post_id=' + id, view=web.db.SQLLiteral('view+1'))
        return forum_render.topic(
                id,
                model.getbysql(
                    'select * from forum_posts as a, member_info as b where a.username = b.member_username and a.post_id = $x',
                    vars={'x':id}
                    ),
                model.getbysql(
                    'select * from forum_backposts as a, member_info as b where a.username = b.member_username and a.post_id=$x limit $y offset $z',
                    vars={'x':id, 'y':page.page_size, 'z':page.offset}
                    ),
                page
                )

    def POST(self, id):
        if session.login != True:
            raise web.seeother('/message?msg=' + '登录后才可以回帖!'.decode('utf-8'))
        i = web.input(content='')
        if i.content != '':
            model.add('forum_backposts', post_id=id, backpost_content=i.content, username=session.username)
            model.update('forum_posts', where='post_id=' + id, back=web.db.SQLLiteral('forum_posts.back+1'), last_username=session.username, last_time=web.db.SQLLiteral('NOW()'))

        raise web.seeother('/topic/'+id)

# 发帖
class WritePost:
    def GET(self):
        if(session.login != True):
            raise web.seeother('/message?msg=' + '登录后才可以发帖!'.decode('utf-8'))
        return forum_render.write_post()

    def POST(self):
        if(session.login != True):
            raise web.seeother('/message?msg=' + '登录后才可以发帖!'.decode('utf-8'))

        i = web.input(post_type='', subject='', content='')
        if(i.post_type == '' or i.subject=='' or i.content == ''):
            raise web.seeother('/write_post')
        else:
            model.add('forum_posts', post_title=i.subject, post_content=i.content, post_type=i.post_type, username=session.username)
            raise web.seeother('/forum')

# 会员管理
class Member:
    def GET(self):
        if session.login == True and session.username != '':
            return auth_render.member(model.get('member_info', where='member_username="' + session.username + '"'))
        else:
            session.kill()
            raise web.seeother('/login')

    def POST(self):
        i = web.input(email='')
        if session.login == True and session.username != '' and i.email != '':
            model.update('member_info', where='member_username="' + session.username + '"', member_email=i.email)
            raise web.seeother('/member')
        else:
            raise web.seeother('/login')

# 密码修改
class Password:
    def GET(self):
        if session.login == True and session.username != '':
            return auth_render.password()
        else:
            session.kill()
            raise web.seeother('/login')

    def POST(self):
        i = web.input(old_password='', password1='', password2='')
        if session.login == True and session.username != '':
            if i.old_password != '' and i.password1 != '' and i.password2 != '' and tools.check_user(session.username, i.old_password) and i.password1 == i.password2:
                model.update('member_info', where='member_username="' + session.username + '"', member_password=tools.make_password(i.password1))
                raise web.seeother('/')
            else:
                raise web.seeother('/password')
        else:
            raise web.seeother('/message?msg=' + '您未登录!'.decode('utf-8'))

class Message:
    def GET(self):
        i = web.input(msg='')
        return auth_render.message(i.msg)


class Admin:
    def GET(self):
        return admin_render.admin_layout()
    
    def POST(self):
        data = web.input(username='', password='')
        if data.username == 'admin' and data.password != '' and tools.check_user(data.username, data.password):
            session.login = True
            session.username = data.username
            raise web.seeother('/admin')
        raise web.seeother('/message?msg=' + '用户名或密码错误!'.decode('utf-8'))

class NewsAdmin:
    def GET(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input()
        page = Page('/news_admin?', i, model.getcount('news_info'), 5)
        return admin_render.news_admin(
                model.get(
                    'news_info', 
                    order='news_pub_time desc', 
                    limit=page.page_size, 
                    offset=page.offset
                    ), 
                page
                )

    def POST(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input(title='', content='')
        if i.title != '' and i.content != '':
            model.add('news_info', news_title=i.title, news_content=i.content)
            raise web.seeother('/news_admin')
        else:
            raise web.seeother('/message?msg=' + '输入有误!'.decode('utf-8'))

class NewsDelete:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        model.delete('news_info', where='news_id=' + id)
        raise web.seeother('/news_admin')

class ProductAdmin:
    def GET(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input()
        page = Page('/product_admin?', i, model.getcount('product_info'), 5)
        return admin_render.product_admin(
                model.get(
                    'product_info',
                    order='product_date desc',
                    limit=page.page_size,
                    offset=page.offset
                    ),
                page
                )

    def POST(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input(name='', price='', intro='', type='')
        if(i.name != '' and i.price != '' and type != ''):
            model.add('product_info', product_type=i.type, product_name=i.name, product_price=i.price, product_intro=i.intro)
            raise web.seeother('/product_admin')
        else:
            raise web.seeother('/message/msg=' + '输入有误!'.decode('utf-8'))

class ProductDelete:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        model.delete('product_info', where='product_id=' + id)
        raise web.seeother('/product_admin')

class MemberAdmin:
    def GET(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input()
        page = Page('/member_admin?', i, model.getcount('member_info'), 15)
        return admin_render.member_admin(
                model.get(
                    'member_info',
                    limit=page.page_size,
                    offset=page.offset
                    ),
                page
                )

class MemberDelete:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        model.delete('member_info', where='member_id=' + id)
        raise web.seeother('/member_admin')


class PostAdmin:
    def GET(self):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input()
        page = Page('/post_admin?', i, model.getcount('forum_posts'), 15)
        return admin_render.post_admin(
                model.get(
                    'forum_posts',
                    order='post_pub_time desc',
                    limit=page.page_size,
                    offset=page.offset
                    ),
                page
                )

class PostDelete:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        model.delete('forum_posts', where='post_id=' + id)
        raise web.seeother('/post_admin')


class BackpostAdmin:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input()
        page = Page('/backpost_admin/' + id + '?', i, model.getcount('forum_backposts', where='post_id=' + id), 15)
        return admin_render.backpost_admin(
                model.get(
                    'forum_backposts',
                    where='post_id=' + id,
                    order='backpost_pub_time desc',
                    limit=page.page_size,
                    offset=page.offset
                    ),
                page
                )

class BackpostDelete:
    def GET(self, id):
        if not tools.is_admin_login():
            raise web.seeother('/message?msg=' + '你不是管理员!'.decode('utf-8'))
        i = web.input(post_id='')
        model.delete('forum_backposts', where='backpost_id=' + id)
        raise web.seeother('/backpost_admin/' + i.post_id)
