##算法文件


#这里导入需要的包以及数据库
#from .models import  数据库名

#贫困生算法
def algorithm_poor():

    return 0

#综合能力算法
def algorithm_ability():

    return 0

#成绩预测算法
def algorithm_grade():
    return 0

#学生监测总页面算法
def algorithm_descrip(term,stu_id):
    from .models import student_rank,student_grade
    print('this term is :', term)
    jidian = []
    xuefen = []
    year_name = []
    zonghe = []
    paiming=[]
    paiming1=[]
    temp_zonghe = student_rank.objects.filter(term=term)
    if len(temp_zonghe) > 0:
        year_name = temp_zonghe[0].year
        zhiyu = str(temp_zonghe[0].zhiyu_rank).split('/')
        deyu = str(temp_zonghe[0].deyu_rank).split('/')
        tiyu = temp_zonghe[0].tiyu_score
        chuangxin = temp_zonghe[0].chuangxin_score
        zh = str(temp_zonghe[0].zonghe_rank).split('/')
        zonghe.append([int((1.0 - float(zhiyu[0]) / float(zhiyu[1])) * 100) + 1,
                       int((1.0 - float(deyu[0]) / float(deyu[1])) * 100) + 1,
                       float(tiyu), float(chuangxin),
                       int((1.0 - float(zh[0]) / float(zh[1])) * 100) + 1])
    else:
        zonghe = ["false"]
    temp_grade = student_grade.objects.filter(user_id=stu_id).order_by("term")
    for temp in temp_grade:
        jidian.append(temp.jidian)
        xuefen.append(temp.xuefen)
        paiming1.append(temp.paiming)
    for a in paiming1:
        b=str(a).split('/')
        paiming.append(round(int(b[0])/int(b[1]),2))
    return jidian,xuefen,zonghe,year_name,paiming

#学生画像以及基本信息
def algorithm_Ssbase_info(account):
    from .models import student_info
    base_info = (student_info.objects.filter(s_id=account))[0]
    img_url = "/static/image/base_image/" + str(account) + ".jpg"
    '''
        ===读取信息=== 
    若平均排名位于前5%，为学霸；
    周图书馆到访率大于5次，为图书馆常客；
    体育成绩高于90分为体育大人；
    每周运动打卡超过10小时为运动健将；
    连续三学期担任班干部或部长级别职务的为办事小能手
        。。。
        。。。
    '''
    huaxiang='学霸,图书馆常客,体育达人'
    return base_info,img_url,huaxiang

