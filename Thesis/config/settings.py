import web
from code import session

web.config.debug = True

db = web.database(dbn='mysql', db='thesis_ubuntu', user='root', passwd='123456')

render = web.template.Render('templates', base='layout')

forum_render = web.template.Render(
                                    'templates/forum/', 
                                    base='forum_layout', 
                                    globals={'datestr':web.datestr, 'session':session}
                                    )

auth_render = web.template.Render(
                                    'templates/auth/',
                                    base='auth_layout',
                                    globals={'datestr':web.datestr, 'session':session}
                                    )

admin_render = web.template.Render(
                                    'templates/admin/',
                                    globals={'datestr':web.datestr, 'session':session}
                                    )
