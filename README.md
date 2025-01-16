# ○○ 마켓
○○대학교 학생들의 중고물품 거래 플랫폼 


## 🖥️ 프로젝트 소개
2023 ○○대학교 SW Week 오픈소스 웹 해커톤 경연대회
○○대학교 학생들의 중고물품 거래 플랫폼 이라는 주제로 1박2일동안 진행
<br>


### ⚙️ 개발 환경
- `Python 3.11`
- `Django`
- **Library** :  Beautifulsoup, gunicorn
- **Database** : PostgreSQL
- **Environment** : Docker, Nginx, SSL, AWS EC2


## ❗ 주요 기능
#### 상품 인식 및 카테고리 자동 분류 기능
#### 네이버 카페 ‘중고나라’ 상품 시세 크롤링 기능
#### SMTP 메일서버를 이용한 사용자 등록 기능
<br>

## 🧬 System Architecture

![image](https://github.com/MegaZizon/Hackathon20231031/assets/105596059/1d6ad761-831a-4fb1-ad35-3b07769fa84a)

---

<details><summary> <h3>🧾 자세히</h3> </summary>
 
---
 
## 🌕 메인 로직 


 가비아 웹 호스팅 업체에서 ciasom.shop 도메인 호스팅 받아 사용하였다.

 호스팅된 도메인은 AWS Route 53에서 AWS EC2 인스턴스로 라우팅 하였다.

 SSL/TLS 인증서를 발급받아 HTTPS를 적용하기 위해 nginx에서 certbot을 구성하여 Let’s Encrypt 서비스를 이용하여 인증서를 발급받았다.

 EC2 인스턴스에서 Docker를 설치한 뒤 Docker Container에서 Nginx, Postgre, Gunicorn과 Django를 실행하여 웹 서버를 구축하였다.

 nginx 에서 받은 사용자의 request를 장고 서버로 바로 보내면 배포 단계에서는 성능이나 효율상 문제가 있어 gunicorn과 같은 CGI의 일종인 WSGI(Web Server Gateway Interface)가 필요하다.

 WSGI는 멀티 쓰레드(multi-thread)를 생성할 수 있어 클라이언트 요청이 많아도 효율적으로 처리할 수 있다.

 WSGIApplication(Gunicorn)이 시작하면 워커(자식 프로세스)를 생성한다. 메인 쓰레드는 while문을 돌면서 워커들을 관리하며 각각 워커가 WSGIServer를 시작한다.

 WSGIServer의 핸들러인 WSGIHandler가 웹서버 요청을 받아 장고에 전달 후 결과를 받아 웹 서버에 응답한다.

 HTTPS로 온 사용자 요청은 Nginx에서 정적인 파일을 제공받고 gunicorn을 통해 동적인 로직을 제공받아 페이지가 표시된다.

## 🌙 상세 로직 


 사용자에게 인증 요청이 오면 구글 SMTP 서버를 사용하여 인증을 보낸다.

 사용자에게 카테고리 분류 요청이 오면 http://aiopen.etri.re.kr:8000/ObjectDetect에 이미지를 base64로 인코딩하여 API키와 함께 request를 보내 json으로 응답을 받은 뒤. 정확도가 0.8 이상일 경우 사용자에게 문자열을 응답한다.

 사용자에게 시세 검색 요청이 오면 https://web.joongna.com/search/{물품명}?sort=RECENT_SORT (물품 검색)에 request 를 보내 HTML을 BeautifulSoup로 파싱한 뒤 id값이 product-item-price-title-1인 요소(상품 가격)를 선택한다.

 시세 데이터들 중에서 이상치를 제거하고 유효한 값들만 남긴뒤 이 정보를 사용자에게 전송한다. 
 
 
</details>

---

## 🔗 API 기능 명세서
  
![image](https://github.com/MegaZizon/Hackathon20231031/assets/105596059/4a7d1517-7a9c-4854-89fa-d0e5f9bbcf0b)



---

## 🗂️ DB 스키마

![image](https://github.com/MegaZizon/Hackathon20231031/assets/105596059/d62918be-4293-464f-a18e-f1562ff3c182)


---
<!-- ## 🚩 구현 결과



#### 시연영상

https://youtu.be/rCbfpVIXRxY![image](https://github.com/MegaZizon/Hackathon20231031/assets/105596059/36f36c91-43bc-4ee5-9b13-836fb6a1d4ef)
-->


