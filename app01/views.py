import datetime
from django.core import serializers
from django.core.serializers import serialize
from django.contrib.sessions import serializers
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
from app01 import models
from django.db.models import Sum, Count
from django.contrib import auth

from django.contrib.auth.decorators import login_required
import json
from geetest import GeetestLib
from app01 import forms
from app01.models import UserInfor
import time
from rbac.service.perssions import initial_session
# 后台房间列表显示


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "67e8343bf6024db330680b4dd70c0bd0"
pc_geetest_key = "2cbedf94513e238e43eef4051efc580e"


def admin_login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]

        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                #注册权限到session中
                print("user",user)
                initial_session(user,request)
                ret["msg"] = "/admin_index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "admin_login.html")


def get_geetest(request):
    user_id = request.user.pk
    # print("user_id:",user_id)
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    # print("user_id-geetest",user_id)
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 注册的视图函数
def admin_register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfor.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/admin_index/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "admin_register.html", {"form_obj": form_obj})

    # 校验用户名是否已被注册


def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    print(username)
    is_exist = models.UserInfor.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册！"
    return JsonResponse(ret)


def admin_index(request):
    return HttpResponse("...ok")

def admin_userinfor(request):

    return HttpResponse("userinfor")

def admin_logout(request):
    auth.logout(request)
    return redirect("/login/")


def admin_house(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.houseAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/admin_house/", max_page=9, )

    ret = models.houseAccount.objects.all().order_by("-day_time", "-id")[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "admin_houselist.html", {"house_list": ret, "page_html": page_html})
    # now = datetime()
    # print(now)
    # ret = models.houseAccount.objects.all().order_by("id")
    # return render(request,"admin_houselist.html",{"house_list":ret})


# 添加住房
def admin_addhouse(request):
    error_msg = ""
    if request.method == "POST":
        new_house_name = request.POST.get("house_name", None)
        new_house_sex = request.POST.get("house_sex", None)
        new_house_id = request.POST.get("house_id", None)
        new_house_cata = request.POST.get("cata_list", None)
        new_house_num = request.POST.get("house_num", None)
        new_house_time = request.POST.get("house_time", None)
        new_house_price = request.POST.get("house_price", None)
        new_dayTime = request.POST.get("dayTime", None)
        new_house_remark = request.POST.get("house_remark", None)
        models.houseAccount.objects.create(name=new_house_name, sex=new_house_sex,
                                           identity=new_house_id, cata_house_id=new_house_cata,
                                           num_house=new_house_num, day_house=new_house_time,
                                           price_house=new_house_price, day_time=new_dayTime,
                                           remark_house=new_house_remark)
        return redirect("/admin_house/")

    # when requesting pages, back last page
    cata_ret = models.cataHouse.objects.all().order_by("id")
    return render(request, "admin_addhouse.html", {"error": error_msg, "cata_list": cata_ret})


# 编辑住房
def admin_edithouse(request):
    if request.method == "POST":
        # ======get laste========
        new_house_id = request.POST.get("id", None)
        new_house_name = request.POST.get("house_name", None)
        new_house_sex = request.POST.get("house_sex", None)
        new_house_idcar = request.POST.get("house_id", None)
        new_house_cata = request.POST.get("cata_list", None)
        new_house_num = request.POST.get("house_num", None)
        new_house_time = request.POST.get("house_time", None)
        new_house_price = request.POST.get("house_price", None)
        new_dayTime = request.POST.get("dayTime", None)
        new_house_remark = request.POST.get("house_remark", None)
        # ========update=========
        edit_house_obj = models.houseAccount.objects.get(id=new_house_id)
        edit_house_obj.name = new_house_name
        edit_house_obj.sex = new_house_sex
        edit_house_obj.identity = new_house_idcar
        edit_house_obj.cata_house_id = new_house_cata
        edit_house_obj.num_house = new_house_num
        edit_house_obj.day_house = new_house_time
        edit_house_obj.price_house = new_house_price
        edit_house_obj.day_time = new_dayTime
        edit_house_obj.remark_house = new_house_remark
        edit_house_obj.save()
        return redirect("/admin_house/")

    edit_id = request.GET.get("id")
    if edit_id:
        edit_house = models.houseAccount.objects.get(id=edit_id)
        ret = models.cataHouse.objects.all()
        return render(request, "admin_edithouse.html", {"cata_list": ret, "house_obj": edit_house})
    else:
        return HttpResponse("Unsuccess")


# 删除住房
def admin_delhouse(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.houseAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_house/")
    else:
        return HttpResponse("data not exist")


# 后台洗澡列表显示========================================

def admin_bath(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.bathAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/admin_bath/", max_page=9, )
    # print("bath:",page_obj.end)
    ret = models.bathAccount.objects.all().order_by("-day_bath", "-id")[page_obj.start:page_obj.end]
    # print("ret:",ret)
    page_html = page_obj.page_html()
    # ret = models.bathAccount.objects.all().order_by("id")
    return render(request, "admin_bathlist.html", {"bath_list": ret, "page_html": page_html})


# 添加洗浴
def admin_addbath(request):
    error_msg = ""
    if request.method == "POST":
        new_bath_num = request.POST.get("bath_num", None)
        new_bath_back = request.POST.get("bath_back", None)
        new_bath_price = request.POST.get("bath_price", None)
        new_bath_time = request.POST.get("bath_time", None)
        new_bath_remark = request.POST.get("bath_remark", None)
        models.bathAccount.objects.create(num_bath=new_bath_num, num_back=new_bath_back,
                                          price_bath=new_bath_price, day_bath=new_bath_time,
                                          remar_bath=new_bath_remark)
        return redirect("/admin_bath/")

    # when requesting pages, back last page
    return render(request, "admin_addbath.html", {"error": error_msg})


# 删除洗浴
def admin_delbath(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.bathAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_bath/")
    else:
        return HttpResponse("data not exist")
    return render(request, "admin_bathlist.html")


# 编辑洗浴
def admin_editbath(request):
    if request.method == "POST":
        # ======get laste========
        new_bath_id = request.POST.get("id", None)
        new_bath_num = request.POST.get("bath_num", None)
        new_bath_back = request.POST.get("bath_back", None)
        new_bath_price = request.POST.get("bath_price", None)
        new_bath_time = request.POST.get("bath_time", None)
        new_bath_remark = request.POST.get("bath_remark", None)
        # ========update=========
        edit_bath_obj = models.bathAccount.objects.get(id=new_bath_id)
        edit_bath_obj.num_bath = new_bath_num
        edit_bath_obj.num_back = new_bath_back
        edit_bath_obj.price_bath = new_bath_price
        edit_bath_obj.day_bath = new_bath_time
        edit_bath_obj.remark_bath = new_bath_remark
        edit_bath_obj.save()
        return redirect("/admin_bath/")

    edit_id = request.GET.get("id")
    if edit_id:
        edit_bath = models.bathAccount.objects.get(id=edit_id)
        return render(request, "admin_editbath.html", {"bath_obj": edit_bath})
    else:
        return HttpResponse("Unsuccess")


# 支出显示
def admin_expensive(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.expenseAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/admin_expensive/", max_page=9, )

    ret = models.expenseAccount.objects.all().order_by("-day_expense", "-id")[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "admin_expensivelist.html", {"expensive_obj": ret, "page_html": page_html})


# 删除支出
def admin_delexpen(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.expenseAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_expensive/")
    else:
        return HttpResponse("data not exist")
    return render(request, "admin_expensivelist.html")


# 添加支出
def admin_addexpense(request):
    error_msg = ""
    if request.method == "POST":
        new_expenCate = request.POST.get("expense_cata", None)
        new_priceAccount = request.POST.get("expense_money", None)
        new_remarkAccount = request.POST.get("expense_remark", None)
        new_dayTime = request.POST.get("dayTime", None)
        models.expenseAccount.objects.create(expen_cate=new_expenCate, price_account=new_priceAccount,
                                             remark_account=new_remarkAccount, day_expense=new_dayTime)
        return redirect("/admin_expensive/")

    # when requesting pages, back last page
    return render(request, "admin_addexpense.html", {"error": error_msg})


# 编辑支出
def admin_editexpen(request):
    if request.method == "POST":
        # ======get laste========
        new_expense_id = request.POST.get("id")
        new_expense_cata = request.POST.get("expense_cata", None)
        new_expense_money = request.POST.get("expense_money", None)
        new_dayTime = request.POST.get("dayTime", None)
        new_expense_remark = request.POST.get("expense_remark", None)
        # ========update=========
        edit_expense_obj = models.expenseAccount.objects.get(id=new_expense_id)
        edit_expense_obj.expen_cate = new_expense_cata
        edit_expense_obj.price_account = new_expense_money
        edit_expense_obj.day_expense = new_dayTime
        edit_expense_obj.remark_account = new_expense_remark
        edit_expense_obj.save()
        return redirect("/admin_expensive/")

    edit_id = request.GET.get("id")
    if edit_id:
        edit_expense = models.expenseAccount.objects.get(id=edit_id)
        return render(request, "admin_editexpense.html", {"expense_obj": edit_expense})
    else:
        return HttpResponse("Unsuccess")


# 每日收入
def admin_today_income(request):
    error_msg = ""
    ctime = time.strftime('%Y-%m-%d')
    # total_bath = models.bathAccount.objects.filter(dayBath=ctime).aggregate(bath=Sum('priceBath'))
    total_bath = models.bathAccount.objects.filter(day_bath=ctime).aggregate(bath=Sum('price_bath'))
    if total_bath['bath']:
        total_bathn = total_bath['bath']
    else:
        total_bathn = 0

    total_numback = models.bathAccount.objects.filter(day_bath=ctime).aggregate(back=Sum('num_back'))
    if total_numback['back']:
        total_numbackn = total_numback['back']
    else:
        total_numbackn = 0
    print(total_numbackn)

    total_incomebath = total_bathn - total_numbackn * 10  # 除去搓背的洗浴收入

    total_house = models.houseAccount.objects.filter(day_time=ctime).aggregate(house=Sum('price_house'))
    if total_house['house']:
        total_housen = total_house['house']
    else:
        total_housen = 0
    total_Store = models.storeAccount.objects.filter(day_store=ctime).aggregate(store=Sum('price_store'))
    if total_Store['store']:
        total_Store = total_Store['store']
    else:
        total_Store = 0
    total_other = models.otherAccount.objects.filter(day_other=ctime).aggregate(other=Sum('price_other'))
    if total_other['other']:
        total_other = total_other['other']
    else:
        total_other = 0

    total_bathStoreHouse = total_housen + total_incomebath + total_Store + total_other  # 洗浴收入、住房收入、其他收入和百货收入

    total_pay = models.expenseAccount.objects.filter(day_expense=ctime).aggregate(
        expense=Sum('price_account'))
    if total_pay['expense']:
        total_payn = total_pay['expense']
    else:
        total_payn = 0

    total_income = total_bathStoreHouse - total_payn  # 每日净收入

    models.incomeAccount.objects.create(day_income=ctime, total_bath=total_incomebath,
                                        total_bath_house=total_bathStoreHouse, total_house=total_housen,
                                        total_pay=total_payn, total_income=total_income, total_store=total_Store)

    return redirect("/admin_income/")


def admin_day_income(request):
    error_msg = ""

    if request.method == "POST":
        new_dayincome = request.POST.get("dayincome_time", None)

        total_bath = models.bathAccount.objects.filter(day_bath=new_dayincome).aggregate(bath=Sum('price_bath'))
        if total_bath['bath']:
            total_bathn = total_bath['bath']
        else:
            total_bathn = 0

        total_numback = models.bathAccount.objects.filter(day_bath=new_dayincome).aggregate(back=Sum('num_back'))
        if total_numback['back']:
            total_numbackn = total_numback['back']
        else:
            total_numbackn = 0
        print(total_numbackn)

        total_incomebath = total_bathn - total_numbackn * 10  # 除去搓背的洗浴收入

        total_house = models.houseAccount.objects.filter(day_time=new_dayincome).aggregate(house=Sum('price_house'))
        if total_house['house']:
            total_housen = total_house['house']
        else:
            total_housen = 0
        total_Store = models.storeAccount.objects.filter(day_store=new_dayincome).aggregate(store=Sum('price_store'))
        if total_Store['store']:
            total_Store = total_Store['store']
        else:
            total_Store = 0
        total_other = models.otherAccount.objects.filter(day_other=new_dayincome).aggregate(other=Sum('price_other'))
        if total_other['other']:
            total_other = total_other['other']
        else:
            total_other = 0

        total_bathStoreHouse = total_housen + total_incomebath + total_Store + total_other  # 洗浴收入、住房收入、其他收入和百货收入

        total_pay = models.expenseAccount.objects.filter(day_expense=new_dayincome).aggregate(
            expense=Sum('price_account'))
        if total_pay['expense']:
            total_payn = total_pay['expense']
        else:
            total_payn = 0

        total_income = total_bathStoreHouse - total_payn  # 每日净收入

        models.incomeAccount.objects.create(day_income=new_dayincome, total_bath=total_incomebath,
                                            total_bath_house=total_bathStoreHouse, total_house=total_housen,
                                            total_pay=total_payn, total_income=total_income, total_store=total_Store)
        return redirect("/admin_income/")
    return render(request, "admin_dayincome.html", {"error": error_msg})


def admin_income(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.incomeAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/admin_income/", max_page=9, )

    ret = models.incomeAccount.objects.all().order_by("-day_income", "-id")[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "admin_incomelist.html", {"income_list": ret, "page_html": page_html})


def admin_delincome(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.incomeAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_income/")
    else:
        return HttpResponse("data not exist")
    return render(request, "admin_incomelist.html")


def admin_echart_income(request):
    # ctime = time.strftime('%Y-%m-%d')
    ret = models.incomeAccount.objects.all().order_by("day_income", "id")
    # ret = serialize("json",ret)
    # print(ret)

    json_list = []

    for i in ret:
        json_dict = {}
        json_dict["id"] = i.id
        json_dict["total_income"] = i.total_income
        json_dict["day_income"] = i.day_income
        json_dict["remark_income"] = i.remark_income
        json_dict["total_bath"] = i.total_bath
        json_dict["total_bath_house"] = i.total_bath_house
        json_dict["total_house"] = i.total_house
        json_dict["total_pay"] = i.total_pay
        json_dict["total_store"] = i.total_store

        json_list.append(json_dict)

    ret1 = json.dumps(json_list)
    # ret1 = serialize("json", ret)
    # print(ret1,type(ret1))
    return render(request, 'admin_chart_income.html', {"ret": json.dumps(ret1)})


def admin_store(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.storeAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/adminStore/", max_page=9, )

    ret = models.storeAccount.objects.all().order_by("-day_store", "-id")[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "admin_storelist.html", {"store_list": ret, "page_html": page_html})


def admin_addstore(request):
    error_msg = ""
    if request.method == "POST":
        new_store_cata = request.POST.get("store_cata", None)
        new_store_price = request.POST.get("store_price", None)
        new_store_time = request.POST.get("store_time", None)
        new_store_remark = request.POST.get("store_remark", None)
        models.storeAccount.objects.create(cata_store=new_store_cata, price_store=new_store_price,
                                           day_store=new_store_time,
                                           remark_store=new_store_remark)
        return redirect("/admin_store/")

    # when requesting pages, back last page
    return render(request, "admin_addstore.html", {"error": error_msg})


def admin_delstore(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.storeAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_store/")
    else:
        return HttpResponse("data not exist")
    return render(request, "admin_storelist.html")


def admin_editstore(request):
    if request.method == "POST":
        # ======get laste========

        new_store_id = request.POST.get("id", None)
        new_store_cata = request.POST.get("store_cata", None)
        new_store_price = request.POST.get("store_price", None)
        new_store_time = request.POST.get("store_time", None)
        new_store_remark = request.POST.get("store_remark", None)
        # ========update=========
        edit_store_obj = models.storeAccount.objects.get(id=new_store_id)
        edit_store_obj.cata_store = new_store_cata
        edit_store_obj.price_store = new_store_price
        edit_store_obj.day_store = new_store_time
        edit_store_obj.remark_store = new_store_remark
        edit_store_obj.save()
        return redirect("/admin_store/")

    edit_id = request.GET.get("id")
    if edit_id:
        edit_store = models.storeAccount.objects.get(id=edit_id)
        return render(request, "admin_editstore.html", {"store_obj": edit_store})
    else:
        return HttpResponse("Unsuccess")


def admin_other(request):
    page_num = request.GET.get("page")
    print(page_num, type(page_num))

    # 总数据是多少
    total_count = models.otherAccount.objects.all().count()
    # print(total_count)
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="/adminOther/", max_page=9, )

    ret = models.otherAccount.objects.all().order_by("-day_other", "-id")[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "admin_otherlist.html", {"other_list": ret, "page_html": page_html})


def admin_delsother(request):
    del_id = request.GET.get("id", None)
    if del_id:
        del_obj = models.otherAccount.objects.get(id=del_id)
        del_obj.delete()
        return redirect("/admin_other/")
    else:
        return HttpResponse("data not exist")
    return render(request, "admin_storelist.html")


def admin_editother(request):
    if request.method == "POST":
        # ======get laste========

        new_other_id = request.POST.get("id", None)
        new_other_cata = request.POST.get("other_cata", None)
        new_other_price = request.POST.get("other_price", None)
        new_other_time = request.POST.get("other_time", None)
        new_other_remark = request.POST.get("other_remark", None)
        # ========update=========
        edit_other_obj = models.otherAccount.objects.get(id=new_other_id)
        edit_other_obj.cata_other = new_other_cata
        edit_other_obj.price_other = new_other_price
        edit_other_obj.day_other = new_other_time
        edit_other_obj.remark_other = new_other_remark
        edit_other_obj.save()
        return redirect("/admin_other/")

    edit_id = request.GET.get("id")
    if edit_id:
        edit_other = models.otherAccount.objects.get(id=edit_id)
        return render(request, "admin_editother.html", {"other_obj": edit_other})
    else:
        return HttpResponse("Unsuccess")


def admin_addother(request):
    error_msg = ""
    if request.method == "POST":
        new_other_cata = request.POST.get("other_cata", None)
        new_other_price = request.POST.get("other_price", None)
        new_other_time = request.POST.get("other_time", None)
        new_other_remark = request.POST.get("other_remark", None)
        models.otherAccount.objects.create(cata_other=new_other_cata, price_other=new_other_price,
                                           day_other=new_other_time,
                                           remark_other=new_other_remark)
        return redirect("/admin_other/")

    # when requesting pages, back last page
    return render(request, "admin_addother.html", {"error": error_msg})
