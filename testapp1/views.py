from django.shortcuts import render,redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from random import *
from .sendmail import send
from django.conf import settings
from django.http import HttpResponse ,HttpResponseRedirect
from django.http import JsonResponse
import os
from .models import File
from django.http import StreamingHttpResponse
import urllib3
import json
import base64
import requests
from bs4 import BeautifulSoup
import numpy as np


def write(request):
    if request.method == 'POST':  
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = '_media/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = Temp_File_Path()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    document = File(file_path=fileName,file_name=fileName)
                    document.save()
                    FileFolder.delete()
                    
                    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
                    accessKey = "bf46f45a-d268-4e8b-b309-5b80a5520d92"
                    imageFilePath = os.path.join(settings.MEDIA_ROOT, fileName)
                    type = "IMAGE_FILE_TYPE"

                    file = open(imageFilePath, "rb")
                    imageContents = base64.b64encode(file.read()).decode("utf8")
                    file.close()

                    requestJson = {
                        "argument": {
                            "type": type,
                            "file": imageContents
                        }
                    }

                    http = urllib3.PoolManager()
                    response = http.request(
                        "POST",
                        openApiURL,
                        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
                        body=json.dumps(requestJson)
                    )

                    result = json.loads(response.data.decode("utf-8"))
                    print("result:",result)
                    detected_class = False
                    detected_class_data = None
                    if "return_object" in result and "data" in result["return_object"]:
                        data = result["return_object"]["data"]
                        i=0
                        for item in data:
                            confidence = float(item["confidence"])
                            if confidence >= 0.8:
                                if i == 1:
                                    detected_class = False
                                    break
                                if detected_class == "person":
                                    continue
                                detected_class_data = item["class"]
                                print(f"Detected class: {detected_class}")
                                detected_class = True
                                i += 1
                    else:
                        print("No valid data found in the response.")
                        detected_class=False

                    if detected_class:
                        print(detected_class_data)
                        res = JsonResponse({'data':'업로드 성공 및 카테고리 분류 성공!','existingPath': fileName,'category':detected_class_data})   
                    else:
                        res = JsonResponse({'data':'업로드에 성공하였으나, 카테고리를 지정하지 못하였습니다.','existingPath':fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            else:
                path = '_media/' + existingPath
                model_id = Temp_File_Path.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                            document = File(file_path=model_id.name,file_name=fileName)
                            document.save()
                            model_id.delete()


                            openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
                            accessKey = "bf46f45a-d268-4e8b-b309-5b80a5520d92"
                            imageFilePath = imageFilePath = os.path.join(settings.MEDIA_ROOT, fileName)
                            type = "IMAGE_FILE_TYPE"

                            file = open(imageFilePath, "rb")
                            imageContents = base64.b64encode(file.read()).decode("utf8")
                            file.close()

                            requestJson = {
                                "argument": {
                                    "type": type,
                                    "file": imageContents
                                }
                            }

                            http = urllib3.PoolManager()
                            response = http.request(
                                "POST",
                                openApiURL,
                                headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
                                body=json.dumps(requestJson)
                            )

                            result = json.loads(response.data.decode("utf-8"))
                            print("result:",result)
                            detected_class = False
                            detected_class_data = None
                            if "return_object" in result and "data" in result["return_object"]:
                                data = result["return_object"]["data"]
                                i=0
                                for item in data:
                                    confidence = float(item["confidence"])
                                    if confidence >= 0.8:
                                        if i == 1:
                                            detected_class = False
                                            break
                                        if detected_class == "person":
                                            continue
                                        detected_class_data = item["class"]
                                        print(f"Detected class: {detected_class}")
                                        detected_class = True
                                        i += 1
                            else:
                                print("No valid data found in the response.")
                                detected_class=False

                            if detected_class:
                                print(detected_class_data)
                                res = JsonResponse({'data':'업로드 성공 및 카테고리 분류 성공!','existingPath': fileName,'category':detected_class_data})   
                            else:
                                res = JsonResponse({'data':'업로드에 성공하였으나, 카테고리를 지정하지 못하였습니다.','existingPath':fileName})

                        else:
                            res = JsonResponse({'existingPath':model_id.existingPath})
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
    return render(request, 'main/product_write.html')


def upload_img(request, filename):
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    def file_iterator(image_path, chunk_size=20000000):
        with open(image_path, 'rb') as image_file:
            while True:
                chunk = image_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(file_iterator(image_path))
    response['Content-Type'] = 'image/jpeg'  # 이미지 형식에 맞게 수정
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


def mypage(request):
    user_id=request.session['user_id']
    user=User.objects.get(user_id=user_id)
    post=Post.objects.filter(user_id=user_id)
    content = {"post":post,"user":user}
    return render(request,'main/mypage.html',content)

def search(request,searchStr):
    if(searchStr=="전체보기"):
        post=Post.objects.all().order_by('-id')
        content = {"search_post":post,"search_str":searchStr}
        return render(request,'main/search.html',content)
    search_post=Post.objects.filter(title__contains=searchStr)
    content = {"search_post":search_post,"search_str":searchStr}
    return render(request,'main/search.html',content)

def cost(request,cost):
    search_str=cost
    url = f"https://web.joongna.com/search/{cost}?sort=RECENT_SORT"

    # 웹 페이지 요청
    response = requests.get(url)

    # 응답이 정상인 경우
    if response.status_code == 200:
        # 웹 페이지의 HTML 내용을 BeautifulSoup로 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 아이디가 "product-item-price-title-1"인 요소를 선택
        element_list = soup.find_all("div","font-semibold space-s-2 mt-0.5 text-heading lg:text-lg lg:mt-1.5")
        element = soup.find("span","font-bold text-2xl mr-1 max-[599px]:text-xl")
        print(element_list)
        element_list_array = []
        for child in element_list:
            price_text = child.get_text()
            price_text = price_text.replace("원", "")
            price_text = price_text.replace(",", "")
            print(price_text)
            element_list_array.append(int(price_text))
        print("element_list:",element_list_array)
        element= element.get_text()
        element= element.replace("원", "")
        element= element.replace(",", "")
        print("avg:",int(element))
        
        
        sorted_data = sorted(element_list_array)

        Q1 = np.percentile(sorted_data, 25)
        Q3 = np.percentile(sorted_data, 75)
        
        # IQR 계산
        IQR = Q3 - Q1
        
        # 이상치 범위 정의
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # 이상치 식별
        outliers = [x for x in sorted_data if x < lower_bound or x > upper_bound]
        
        # 이상치 제거
        valid_data = [x for x in sorted_data if x >= lower_bound and x <= upper_bound]
        
        
        mean = np.mean(valid_data)
        std_dev = np.std(valid_data)

        shold =  3*std_dev
        valid_data = [x for x in valid_data if abs(x - mean) < shold]
        outliers = [x for x in valid_data if abs(x - mean) >= shold]

        print("유효한 데이터:", valid_data)
        print("이상치:", outliers)
        sorted_data = sorted(valid_data)
        
        average_price = sum(sorted_data) / len(sorted_data)
        
        first_calculation_avg = average_price
        first_calculation_least=sorted_data[0]
        print("중고나라 평균 가격:",int(element))

        
        Q1 = np.percentile(sorted_data, 25)
        Q3 = np.percentile(sorted_data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        valid_data = [x for x in sorted_data if x >= lower_bound and x <= upper_bound]
        average_price = sum(valid_data) / len(valid_data)
        least_price = valid_data[0]

        content = {'fir_avg':int(first_calculation_avg),'fir_least':int(sorted_data[0]),
                   'sec_avg':int(average_price),'sec_least':int(least_price),'joongo':int(element),'search_str':search_str}

        print(content)
        return render(request,'main/cost.html',content)



    else:
        return render(request,'main/index.html')

    
    


def post_vote(request, id):
    post = Post.objects.get(id=id)
    post_user = User.objects.get(user_id=post.user_id)
    
    # 추천한 게시글 ID를 쿠키에서 가져옵니다.
    voted_posts = request.COOKIES.get('voted_posts', '').split(',')
    
    uid = request.COOKIES.get('user_id')
    
    if str(id) in voted_posts:
        return JsonResponse({'fail': "fail"})
    else:
        # 중복 투표를 방지하기 위해 쿠키에 게시글 ID 추가
        voted_posts.append(str(id))
        response = JsonResponse({'success': "success", 'vote_count': post.vote})
        
        # 쿠키에 추천한 게시글 ID 저장
        response.set_cookie('voted_posts', ','.join(voted_posts))
        
        # 게시글과 사용자 정보 저장
        post.vote += 1
        post_user.user_score += 1
        post.save()
        post_user.save()
        
        return response


def post_detail(request,id):
    post=Post.objects.get(id=id)
    user_post=Post.objects.filter(user_id=post.user_id)
    user =User.objects.get(user_id=post.user_id)
    post.visited += 1
    post.save()
    content={'post':post,'user_post':user_post,'user':user}

    return render(request,'main/product_details.html',content)

def index(request,content={}):
    
    post=Post.objects.all().order_by('-id')
    content={'posts': post}

    if request.method == "POST":
        print("NO SESSION")
        loginId = request.POST['loginId']
        loginPW = request.POST['loginPW']
        if loginId and loginPW:
            try:
                user = User.objects.get(user_id = loginId)
            except:
                content['error']='아이디를 찾을 수 없습니다.'
                print("NO id")
                return render(request,'main/index.html',content)
            
            if user.user_password == loginPW:
                id=user.user_id+"님 환영합니다."
                content['error']=id
                request.session['user_id'] = user.user_id
                return render(request,'main/index.html',content)
            else:
                content['error']='비밀번호가 틀립니다.'
                print("NO pw")
                return render(request,'main/index.html',content)
    else:
        return render(request,'main/index.html',content)

def signup(request,content={}):
    try:
        content = request.session.get('error')
        del request.session['error']
        if(content=="id"):
            content={"error":"이미 사용중인 아이디 입니다.."}
        elif(content=="email"):
            content={"error":"이미 사용중인 이메일 입니다.."}
        elif(content=="db"):
            content={"error":"데이터 베이스에 등록하던 중 알 수 없는 오류가 발생하였습니다."}
        return render(request,'main/signup.html',content)
    except:
        return render(request,'main/signup.html',content)

def write_submit(request):
    id=request.session['user_id']
    title = request.POST['title']
    price = request.POST['price']
    model_name = request.POST['model_name']
    content = request.POST['content']
    category = request.POST.get("category",default="미등록")
    file = ""
    user=User.objects.get(user_id = id)
    user_nickname=user.user_nickname

    try:
        file = request.FILES['file']
        post = Post(user_id=id,user_nickname=user_nickname,price=price,
                    title=title,content=content,category=category,product_name=model_name,post_img=file)
        post.save()
        print("1111",file)
    except:
        post = Post(user_id=id,user_nickname=user_nickname,price=price,
                    title=title,content=content,category=category,product_name=model_name)
        post.save()
        print("here",file)

    
    
    response = redirect('main_index')
    return response

def join(request):
    id = request.POST['signupId']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    nickname = request.POST['signupNickname']
    img=""
    try:
        img = request.FILES['fileInput']
    except:
        user = User(user_id=id,user_email=email,user_password=pw,user_nickname=nickname)
        user.save()

    print("img:",img)
    if img!="":
        user = User(user_id=id,user_email=email,user_password=pw,user_nickname=nickname,user_img=img)
        user.save()

    
    code=randint(1000,9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code',code)
    response.set_cookie('user_id',user.id)
    send_result = send(email,code)
    if send_result:
        return response
    else:
        return HttpResponse("서버에서 이메일 전송실패.")





def verifyCode(request):
    return render(request, 'sendEmail/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)
        request.session['user_id'] = user.user_id
        return response
    else:
        return redirect('main_verifyCode')
    
    

def logout(request):
    try:
        del request.session['user_id']
        return redirect('main_index')
    except:
        return redirect('main_index')
def check_price(request,searchStr):

    sessionId=request.session['user_id']
    # 검색어를 URL에 추가
    url = f"https://web.joongna.com/search/{searchStr}?sort=RECENT_SORT"

    # 웹 페이지 요청
    response = requests.get(url)

    # 응답이 정상인 경우
    if response.status_code == 200:
        # 웹 페이지의 HTML 내용을 BeautifulSoup로 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 아이디가 "product-item-price-title-1"인 요소를 선택
        element_list = soup.find_all("div","font-semibold space-s-2 mt-0.5 text-heading lg:text-lg lg:mt-1.5")
        element = soup.find("span","font-bold text-2xl mr-1 max-[599px]:text-xl")
        print(element_list)
        element_list_array = []
        for child in element_list:
            price_text = child.get_text()
            price_text = price_text.replace("원", "")
            price_text = price_text.replace(",", "")
            print(price_text)
            element_list_array.append(int(price_text))
        print("element_list:",element_list_array)
        element= element.get_text()
        element= element.replace("원", "")
        element= element.replace(",", "")
        print("avg:",int(element))
        
        
        sorted_data = sorted(element_list_array)

        Q1 = np.percentile(sorted_data, 25)
        Q3 = np.percentile(sorted_data, 75)
        
        # IQR 계산
        IQR = Q3 - Q1
        
        # 이상치 범위 정의
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # 이상치 식별
        outliers = [x for x in sorted_data if x < lower_bound or x > upper_bound]
        
        # 이상치 제거
        valid_data = [x for x in sorted_data if x >= lower_bound and x <= upper_bound]
        
        
        mean = np.mean(valid_data)
        std_dev = np.std(valid_data)

        shold =  3*std_dev
        valid_data = [x for x in valid_data if abs(x - mean) < shold]
        outliers = [x for x in valid_data if abs(x - mean) >= shold]

        print("유효한 데이터:", valid_data)
        print("이상치:", outliers)
        sorted_data = sorted(valid_data)

        average_price = sum(sorted_data) / len(sorted_data)

        # 결과 출력
        print("평균 가격:", int(average_price))
        print("최저 가격:", int(sorted_data[0]))
        print("중고나라 평균 가격:",int(element))



        res = JsonResponse({'avgJoongo':int(element),'avgHallym':int(average_price),'leastHallym':int(sorted_data[0])})
        return res
    else:
        return JsonResponse({'fail':"fail"})