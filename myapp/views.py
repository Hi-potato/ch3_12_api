from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        print(cname)
        # resultList = students.objects.filter(cname = cname) #查詢  //名字要完全依樣，才會顯示
        resultList = students.objects.filter(cname__contains = cname) #查詢 //局部一樣就會顯示
    else:
        
        resultList = students.objects.all().order_by('-cid')
    for item in resultList:
        print(model_to_dict(item))
    # return HttpResponse("Ah~~~~~~HA!")

    errormessage = ""
    # resultList=[]   #模擬查詢結果為空/無資料

    if not resultList:
        errormessage = "No data found"
    #return render(request, 'search_list.html',locals())
    return render(request, 'search_list.html', {'resultList':resultList, 'errormessage':errormessage})

def search_name(request):
    return render(request,'search_name.html')

from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除前後空白
        keywords = site_search.split() #以空白分割成多個關鍵字
        # print(f"site_search={site_search}")
        print(keywords)
        # 一個關鍵字+搜尋一個欄位
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid') #查詢

        # 一個關鍵字+搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cid__contains=site_search) |
        #     Q(cname__contains=site_search) |    
        #     Q(cbirthday__contains=site_search) |
        #     Q(cemail__contains=site_search) |
        #     Q(cphone__contains=site_search) |
        #     Q(caddr__contains=site_search)
        # )
        # resultList=[]

        # 多個關鍵字+搜尋多個欄位 by Codepilot
        # query = Q()
        # for keyword in keywords:
        #     query |=Q(cid__contains=keyword) | Q(cname__contains=keyword) | Q(cbirthday__contains=keyword) | Q(cemail__contains=keyword) | Q(cphone__contains=keyword) | Q(caddr__contains=keyword)
        # resultList = students.objects.filter(query).order_by('cid')
        
        # 多個關鍵字+搜尋多個欄位 by Chat GPT
        q_objects = Q()
        for keyword in keywords:
             q_objects |= (
                Q(cname__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword)
             )


                            # DB 裡 csex 存的是 "M" / "F"
                            # 畫面顯示的是「男 / 女」
                            # 但你想用「男 / 女」當關鍵字搜尋

                            # 👉 問題點：
                            # icontains=keyword 是直接比對資料庫內容，不會自動幫你把「男」轉成 "M"

                            # ✅ 解法一：先轉換關鍵字（最常用）

                            # 在 view 裡先把輸入轉成 DB 值：

                            # if keyword == "男":
                            #     queryset = queryset.filter(csex="M")
                            # elif keyword == "女":
                            #     queryset = queryset.filter(csex="F")
                            # else:
                            #     queryset = queryset.filter(csex__icontains=keyword)

                            # 👉 這是最直覺、最乾淨的做法

                            # ✅ 解法二：用 Q 同時搜尋（比較彈性）

                            # 如果你想讓「男」或「M」都能搜：

                            # from django.db.models import Q

                            # queryset = queryset.filter(
                            #     Q(csex__icontains=keyword) |
                            #     Q(csex="M") if keyword == "男" else
                            #     Q(csex="F") if keyword == "女" else
                            #     Q()
                            # )

                            # （但這寫法比較醜，不太推薦 😅）

                            # ✅ 解法三：建立對照表（推薦進階用）

                            # 如果未來還有更多 mapping：

                            # sex_map = {
                            #     "男": "M",
                            #     "女": "F",
                            # }

                            # if keyword in sex_map:
                            #     queryset = queryset.filter(csex=sex_map[keyword])
                            # else:
                            #     queryset = queryset.filter(csex__icontains=keyword)

                            # 👉 這個最好維護 👍

                            # ⚠️ 重點提醒

                            # 你 template：

                            # {% if data.csex == "M" %}男{% else %}女{% endif %}

                            # 只是「顯示轉換」，
                            # 不會影響資料庫搜尋 ❗

                            # 🚀 最推薦寫法（簡潔版）
                            # sex_map = {"男": "M", "女": "F"}

                            # queryset = queryset.filter(
                            #     csex=sex_map[keyword]
                            # ) if keyword in sex_map else queryset.filter(
                            #     csex__icontains=keyword



        resultList = students.objects.filter(q_objects)

        # 多個關鍵字+搜尋多個欄位 by Tony
        # q_objects = Q()
        # for keyword in keywords:
        #     q_objects.add(Q(cname__contains=keyword), Q.OR)
        #     q_objects.add(Q(csex__contains=keyword), Q.OR)
        #     q_objects.add(Q(cbirthday__contains=keyword), Q.OR)
        #     q_objects.add(Q(cemail__contains=keyword), Q.OR)
        #     q_objects.add(Q(cphone__contains=keyword), Q.OR)
        #     q_objects.add(Q(caddr__contains=keyword), Q.OR)
        # print(q_objects)
        # resultList = students.objects.filter(q_objects)

    else:
        resultList = students.objects.all().order_by('cid')
    for item in resultList:
        print(model_to_dict(item))
    data_count = len(resultList)
    print(f"Total data count:{data_count}")
    status = True
    errormessage = "" 
    if not resultList:
        status = False
        errormessage = "No data found"

    # return HttpResponse("Ah~~~~~~HA!")

    #分頁設定，每頁顯示2筆資料
    paginator = Paginator(resultList,2)
    page_number = request.GET.get('page')  #獲取當前頁碼
    page_obj = paginator.get_page(page_number) #獲取當前頁的資料
    print(f"page_number={page_number}")
    for item in page_obj:
        print(model_to_dict(item))


    return render(request, 'index.html',
                   {'resultList':resultList,
                     'status':status,
                     'errormessage':errormessage,
                     'data_count':data_count,
                     'page_obj':page_obj
                      }
                    )
from django.shortcuts import redirect
def post(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}") #檢查用，資料會印出來
        add = students(cname=cname, csex = csex, cbirthday=cbirthday, cemail=cemail, cphone=cphone, caddr=caddr)    
        #cname=cname 等號左邊橘色的字是MYSQL的欄位，對照models.py；等號右邊白色的字是變數對照 cname = request.POST.get('~~~') 的cname
        add.save()

        # return HttpResponse("已送出 POST 請求")
        return redirect('index')
    else:
        return render(request,'post.html')
    # return HttpResponse("hello")

def edit(request,id):
    print(id)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        
        # orm
        update = students.objects.get(cid=id)
        update.cname=cname
        update.csex=csex
        update.cbirthday=cbirthday
        update.cemail=cemail
        update.cphone=cphone
        update.caddr=caddr
        update.save()
        return redirect('index')
        
        
        return HttpResponse("已送出 POST 請求")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("hello")
        return render(request, 'edit.html', {'obj_data':obj_data} )
    

def delete(request,id):
    print(id)
    # return HttpResponse("hello")
    if request.method == 'POST':
        delete_data = students.objects.get(cid=id)
        delete_data.delete()
        return redirect('index') #定向到index 頁面，顯示更新後的數據列表        
        # return HttpResponse("已送出 POST 請求")
    
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request, 'delete.html', {'obj_data':obj_data} )


from django.http import JsonResponse    
def getAllItems(request):
    resultObject = students.objects.all().order_by('cid')
    # print(type(resultObject))
    # for item in resultObject:
    #     print(model_to_dict(item))
    #     print(type(item))
    resultList = list(resultObject.values()) #將 "querySet, 元素為object" 轉成 "list 元素為dict的型態"
    # print(type(resultList))
    # for item in resultList:
    #     # print(model_to_dict(item))
    #     print(type(item))

    # return HttpResponse("hello")
    return JsonResponse(resultList, safe=False)
    # safe=True, 只允許(丟一層資料)傳入dict
    # safe=False, 只允許傳入非dict



def getItem(request, id):
    try:
        obj = students.objects.get(cid=id)  #篩選，取得單一object
        # print(model_to_dict(obj))
        resultDict = model_to_dict(obj)     #將object轉成dict
        # return HttpResponse("hello")
        return JsonResponse(resultDict, safe=False)
    except:
        # return HttpResponse("False")
        return JsonResponse({"error":"Item not found"},status=404)