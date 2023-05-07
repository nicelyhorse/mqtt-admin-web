from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import time
from .models import user_list
from django.template.loader import get_template

print('============start program successful')


# 查询数据库函数
def my_custom_sql(sql):
    from django.db import connection
    cursor = connection.cursor()
    # 数据检索操作,不需要提交
    cursor.execute(sql)
    row = cursor.fetchall()
    return row


# 登陆注册时查找是否存在该用户名
def findUser(account):
    sql = "select * from user_list where account='{}'".format(account)
    data = my_custom_sql(sql)
    return data


@csrf_exempt  # 注册函数
def Register(request):
    if request.method == 'POST':  #  请求方法为POST时，进行处理
        print("================收到注册请求")
        name = request.POST.get('name')
        account = request.POST.get('user')
        pwd = request.POST.get('pwd')
        data = findUser(account)
        if len(data) == 0:
            registerSql = "insert into user_list values('{}','{}','{}','fcg')". \
                format(name, account, pwd)
            my_custom_sql(registerSql)
            result = 1
        else:
            result = '该账号已被注册，请更换'

        print(result)
        return_json = {
            'result': result
        }
        return HttpResponse(json.dumps(return_json), content_type='application/json')


@csrf_exempt  # 登陆函数
def Log_in(request):
    if request.method == 'POST':  #  请求方法为POST时，进行处理
        print('======收到登录请求=============')
        account = request.POST.get('user')
        pwd = request.POST.get('pwd')
        data = findUser(account)
        if len(data) == 0:
            result = '账号输入错误，请检查'
        else:
            if data[0][2] == pwd:
                result = 1
                request.session['name'] = data[0][0]
                request.session['account'] = data[0][1]
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                print(ip)
                sql = 'insert into login_his(account,ntime,add_ip) values("{}","{}","{}")'. \
                    format(data[0][1], time.strftime("%Y-%m-%d %H:%M:%S"), ip)
                my_custom_sql(sql)
            else:
                result = '密码错误，请检查'
        return_json = {
            'result': result,
            'url': 'Home'
        }
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    else:
        request.session['name'] = ''
        request.session['account'] = ''
        return render(request, 'log_in.html')


# 登录后的主界面
def Home(request):
    if 'name' in request.session:
        name = request.session['name']
        print(name)
        templates = get_template('home.html')
        html = templates.render(locals())  # locals()函数会把当前变量打包成一个字典
        return HttpResponse(html)
    else:
        return render(request, '您尚未登录，请登录')


# =================以下是功能界面函数=====================


@csrf_exempt  # 用户中心
def changeAccount(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        # 查询所有表
        if order == "changeAccount":
            name = request.POST.get('name')
            account = request.POST.get('account')
            pwd = request.POST.get('pwd')
            if account[-12:] == '@myemail.com' and len(account) > 12:
                # 判断信息是否正确
                if len(name) < 1 or len(pwd) < 1:
                    result = "信息格式（所有字段长度须大与1）不正确，请修改后重试"
                else:
                    # 查重
                    data = findUser(account)
                    if len(data) > 0:
                        result = '该域名已经被注册，请重试'
                    else:
                        sql = "UPDATE user_list set user_name='{}',account='{}',pwd='{}' where account='{}';". \
                            format(name, account, pwd, request.session['account'])
                        my_custom_sql(sql)
                        result = '修改成功，点击确认重新登录。'
            else:
                result = '域名不符合规则，域名格式：****@myemail.com'
            return_json = {
                'result': result,
                '': 1,
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == 'getloginHis':
            sql = 'select ntime,add_ip from login_his where account="{}";'.format(request.session['account'])
            print(sql)
            data = my_custom_sql(sql)
            print(data)
            return_json = {
                'data': data,
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        # 查询每张表数据
    else:
        if 'account' in request.session and len(request.session['account']) > 10:
            return render(request, 'changeAccount.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 写信
def writeEmail(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        # 写信
        if order == "writeEmail":
            nfrom = request.session['account']
            nto = request.POST.get('touser')
            emailInfo = request.POST.get('emailInfo').replace('\n', '')
            ntype = request.POST.get('type')
            data = findUser(nto)
            if len(data) < 1:
                result = '发送失败，该邮箱地址尚未注册'
            else:
                ntime = time.strftime("%Y%m%d:%H%M%S")
                sql = "insert into email_list(host,nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}','{}');". \
                    format(nfrom, nfrom, nto, emailInfo, ntype, ntime)
                print(sql)
                my_custom_sql(sql)
                sql = "insert into email_list(host,nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}','{}');". \
                    format(nto, nfrom, nto, emailInfo, ntype, ntime)
                my_custom_sql(sql)
                result = "发送成功"

            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        if order == "saveEmail":
            nfrom = request.session['account']
            nto = request.POST.get('touser')
            emailInfo = request.POST.get('emailInfo')
            ntype = request.POST.get('type')
            sql = "insert into email_list(host,nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}','{}');". \
                format(nfrom, nfrom, nto, emailInfo, ntype, time.strftime("%Y%m%d:%H%M%S"))
            my_custom_sql(sql)
            result = "保存成功"

            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'writeEmail.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 查看邮件列表
def emailList(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        host = request.session['account']
        # 邮件列表
        if order == "getEmailList":
            nto = request.session['account']

            sql = "select ids,nfrom,emailInfo,ntime from email_list where host='{}' and nto='{}' and type='fs'  ORDER BY ntime DESC;".format(
                host, nto)
            print(sql)
            data = my_custom_sql(sql)
            result = []
            for temp in data:
                if len(temp[2]) < 20:
                    info = temp[2]
                else:
                    info = temp[2][:20] + '...'
                result.append([temp[0], temp[1], info, temp[3]])
            print(result)
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "delEmail":
            ids = request.POST.get('ids')
            print('删除', ids)
            sql = "update email_list set type='lj'  where ids='{}' and host='{}';".format(ids, host)
            print(sql)
            data = my_custom_sql(sql)
            result = 1
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'emailList.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 查看已发送列表
def sendEmialList(request):
    if request.method == 'POST':
        host = request.session['account']
        order = request.POST.get('order')
        # 邮件列表
        if order == "sendEmailList":
            nto = request.session['account']
            sql = "select ids,nfrom,emailInfo,ntime  from email_list where host='{}' and nfrom='{}' and type='fs' ORDER BY ntime DESC;".format(
                host, nto)
            data = my_custom_sql(sql)
            result = []
            for temp in data:
                if len(temp[2]) < 20:
                    info = temp[2]
                else:
                    info = temp[2][:20] + '...'
                result.append([temp[0], temp[1], info, temp[3]])
            print(result)
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "delEmail":
            ids = request.POST.get('ids')
            print('删除', ids)
            sql = "update email_list set type='lj'  where ids='{}' and host='{}';".format(ids, host)
            print(sql)
            data = my_custom_sql(sql)
            result = 1
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'sendEmialList.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 查看草稿箱列表
def cgEmialList(request):
    if request.method == 'POST':
        host = request.session['account']
        order = request.POST.get('order')
        # 邮件列表
        if order == "cgEmailList":
            nto = request.session['account']
            sql = "select ids,nto,emailInfo,ntime  from email_list where host='{}' and nfrom='{}' and type='cg' ORDER BY ntime DESC;".format(
                host, nto)
            data = my_custom_sql(sql)
            result = []
            for temp in data:
                if len(temp[2]) < 20:
                    info = temp[2]
                else:
                    info = temp[2][:20] + '...'
                result.append([temp[0], temp[1], info, temp[3]])
            print(result)
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "delEmail":
            ids = request.POST.get('ids')
            print('删除', ids)
            sql = "update email_list set type='lj'  where ids='{}' and host='{}';".format(ids, host)
            print(sql)
            data = my_custom_sql(sql)
            result = 1
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'cgEmialList.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 查看垃圾箱列表
def ljEmialList(request):
    if request.method == 'POST':
        host = request.session['account']
        order = request.POST.get('order')
        # 邮件列表
        if order == "ljEmailList":
            nto = request.session['account']
            # 已发送邮件删除后进入垃圾箱
            sql = "select ids,nfrom,nto,emailInfo,ntime  from email_list where host='{}' and (nfrom='{}' or nto='{}') and type='lj' ORDER BY ntime DESC;".format(
                host, nto, nto)
            # sql = "select ids,nfrom,nto,emailInfo,ntime  from email_list where nfrom='{}' and type='lj' ORDER BY ntime DESC;".format(
            #     nto, nto)
            data = my_custom_sql(sql)
            result = []
            for temp in data:
                if len(temp[3]) < 20:
                    info = temp[3]
                else:
                    info = temp[3][:20] + '...'
                result.append([temp[0], temp[1], temp[2], info, temp[4]])
            print(result)
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "delEmail":
            ids = request.POST.get('ids')
            print('删除', ids)
            sql = "update email_list set type='lj1'  where ids='{}' and host='{}';".format(ids, host)
            print(sql)
            data = my_custom_sql(sql)
            result = 1
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'ljEmialList.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 查看联系人列表
def connect(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        # 邮件列表
        if order == "connect":
            account = request.session['account']
            sql = "select ids,BZ,guest,time from connect where host='{}';".format(account)
            data = my_custom_sql(sql)
            return_json = {
                'result': data
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "delEmail":
            ids = request.POST.get('ids')
            print('删除', ids)
            sql = "delete from connect where ids='{}';".format(ids)
            print(sql)
            data = my_custom_sql(sql)
            result = 1
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        elif order == "add":
            nname = request.POST.get('name')
            naccount = request.POST.get('account')
            print(nname, naccount)
            if len(nname) < 1 or len(naccount) < 1:
                result = '请完善信息'
            else:
                sql = "insert into connect(host,guest,bz,time) values('{}','{}','{}','{}');". \
                    format(request.session['account'], naccount, nname, time.strftime("%Y-%m-%d %H:%M:%S"))
                print(sql)
                data = my_custom_sql(sql)
                result = "添加成功"
            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')

    else:
        if 'account' in request.session and len(request.session['account']) > 12:
            return render(request, 'connect.html')
        else:
            return render(request, '您尚未登录，请登录')


@csrf_exempt  # 重写邮件
def reWriteEmai(request):
    if request.method == 'POST':
        order = request.POST.get('order')
        # 写信
        if order == "writeEmail":
            nfrom = request.session['account']
            nto = request.POST.get('touser')
            emailInfo = request.POST.get('emailInfo')
            ntype = request.POST.get('type')
            data = findUser(nto)
            if len(data) < 1:
                result = '发送失败，该邮箱地址尚未注册'
            else:
                ntime = time.strftime("%Y%m%d:%H%M%S")
                sql = "insert into email_list(host,nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}','{}');". \
                    format(nfrom, nfrom, nto, emailInfo, ntype, ntime)
                print(sql)
                my_custom_sql(sql)
                sql = "insert into email_list(host,nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}','{}');". \
                    format(nto, nfrom, nto, emailInfo, ntype, ntime)
                my_custom_sql(sql)
                result = "发送成功"

            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
        if order == "saveEmail":
            nfrom = request.session['account']
            nto = request.POST.get('touser')
            emailInfo = request.POST.get('emailInfo')
            ntype = request.POST.get('type')
            sql = "insert into email_list(nfrom,nto,emailInfo,type,ntime) values('{}','{}','{}','{}','{}');". \
                format(nfrom, nto, emailInfo, ntype, time.strftime("%Y%m%d:%H%M%S"))
            my_custom_sql(sql)
            result = "保存成功"

            return_json = {
                'result': result
            }
            return HttpResponse(json.dumps(return_json), content_type='application/json')
    ids = request.GET.get('ids')
    sql = "select nto,emailInfo from email_list where ids={}".format(ids)
    print('====================')
    print(sql)
    data = my_custom_sql(sql)
    print(data)
    nto = data[0][0]
    emailInfo = data[0][1].replace('\n', '').replace('\r', '')
    if 'account' in request.session and len(request.session['account']) > 12:
        templates = get_template('reWriteEmai.html')
        html = templates.render(locals())  # locals()函数会把当前变量打包成一个字典
        return HttpResponse(html)
    else:
        return render(request, '您尚未登录，请登录')
