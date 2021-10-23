# ChronicCrawler

# 난 모르겠고 빨리 작동하는거나 보고싶어요

## 설치할 것

rabbitmq-server 설치 (apt)
postgresql 설치 (apt)
그 외 requirements.txt에 추가된것들도 설치 (pip)

## 준비사항

### api 키 넣기

root_of_repo/chroniccrawler/crawler/tools/key.txt를 생성해 key를 넣어주세요.

### postgresql 설치 후 실행하기

```
sudo service postgresql start
```

### 실행 후 psql로 접속하기

```
sudo -u postgres psql
```

### psql에서 chroniccrawler 유저, chroniccrawler 데이터베이스, password도 chroniccrawler로 만들고 chroniccrawler 유저에게 권한 주기

```
CREATE USER chroniccrawler WITH PASSWORD 'chroniccrawler';

CREATE DATABASE chroniccrawler OWNER chroniccrawler;
```

이 시점에서 psql이 열려있는 terminal은 종료해도 됩니다

### rabbitmq-server 실행하기

```
sudo rabbitmq-server
```

이 시점에서 현재 terminal은 종료해도 됩니다

### 마이그레이션 하기

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### django 앱 실행 (실행 유지)

```
python3 manage.py runserver
```

### django 앱의 슈퍼유저 만들기

```
python3 manage.py createsuperuser
```

이후 절차에 따라 슈퍼유저를 만들어주세요.

### 관리자 페이지 접속

대충 아무 인터넷 브라우저나 열어서 접속해주세요. 아마도 127.0.0.1:8000/master 일겁니다.

### 요청할 노선, 정류장 등록하기 (현시점 정류장은 미등록입니다.)

여러 DB가 보일것입니다. 그 중 CHRONICCRAWLER란의 항목 중 Lane to tracks와 Ulsan bus_ lane to tracks에 직접 정보를 등록해야 합니다.

Lane to tracks에 bus name, route id, city code란에 국토교통부 api상의 해당 노선의 정보를 등록해주세요.

Ulsan bus_ lane to tracks에 동일 노선의 울산 BIS api상의 해당 노선의 정보를 등록해주세요.

### celery worker 실행 (실행 유지)

```
celery -A config worker -l INFO
```

### celery beat 실행 (실행 유지)

```
celery -A config beat
```

이 시점에서 자동으로 일정 시간마다 등록한 노선과 정류장에 대한 정보를 요청해 db에 저장할것입니다.

CHRONICCRAWLER의 수동 등록 항목을 제외한 모든 DB 항목은 celery beat가 처음 실행될 때 한번 새로고침되며, Day infos, Node of lanes, Ulsan bus_ time tables는 매일 00:01에 한번, Pos of buss는 매 20초마다 한번 새로고침되도록 설정되어있습니다. 당연히 바꿀 수 있으니 상의 후 바꿔주시기 바랍니다.

# 들어가기

## 시작하기에 앞서

ChronicCrawler는 공공 데이터포털에 공개된 아래 오픈API들을 기반으로 하고 있습니다.

[국토교통부_버스노선정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000758)

[국토교통부_버스위치정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000515)

API Key를 `(앱 위치)/crawler/key.txt`에 저장하세요.

ChronicCrawler는 django와 celery를 활용합니다.

[첫 번째 장고 앱 작성하기](https://docs.djangoproject.com/ko/3.2/intro/tutorial01/)

[첫 번째 장고 셀러리 앱 작성하기](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)

ChronicCrawler는 DB를 활용합니다. migration을 통해 DB를 생성해 주세요.

# Django Models

각 항목의 datatype은 별도의 표시가 없는 한 string입니다.

## LaneToTrack

### 위 모델에 추적할 버스의 정보를 직접 추가해주세요.

bus_name : 버스_번호(??? 방면)  예)337(삼남 순환)

route_id : 국토교통부 버스 api에서 사용하는 버스 노선 id.  예)USB196103373

city_code : 국토교통부 버스 api에서 사용하는 도시코드.  예)26

## NodeOfLane

### 각 버스 노선의 각 정류장과 그 순번에 대한 정보를 가집니다. LaneToTrack에 저장된 각 버스 노선의 정보를 자동으로 가져옵니다.

route_key : LaneToTrack (ForeignKey)

node_order : 해당 노선에서 해당 정류장의 순번. (integer)

node_id : 국토교통부 버스 api에서 사용하는 정류장 id.

node_name : 해당 정류장의 이름.

## PosOfBus

### 각 버스 노선의 현재 운행중인 모든 버스와 그 위치에 대한 정보를 가집니다. LaneToTrack에 저장된 각 버스 노선의 정보를 자동으로 가져옵니다.

route_key : LaneToTrack (ForeignKey)

node_id : (불확실합니다. 정확한 정보를 얻을 시 수정해주세요.)제일 마지막으로 지난 정류장의 국토교통부 버스 api에서 사용하는 정류장 id.

bus_num : 해당 버스의 자동차등록번호.

node_order : 제일 마지막으로 지난 정류장의 해당 노선에서의 순번. (integer)

## DayInfo

### 오늘의 날짜 정보와 공휴일 또는 토요일 등에 대한 정보를 가집니다. 한국천문연구원의 특일정보 api에서 자동으로 가져옵니다.

year : 년도

month : 월

day : 일

name : 해당 날의 이름 (일반 : 주중, 토요일 : 토요일, 일요일 : 일요일, 그 외 공휴일 : api에서 표시해주는 이름 예)한글날)

kind : 해당 날의 종류 (일반 : 0, 토요일 : 1, 일요일 및 공휴일 : 2)

## UlsanBus_LaneToTrack

### LaneToTrack에서 가져오기로 정한 노선들의 추가적인 정보를 가집니다. 울산 BIS api에서 검색해 직접 추가해주세요.

route_key : LaneToTrack (ForeignKey)

route_id : 울산 BIS api에서 사용하는 노선 id.

route_num : 버스 노선 번호.

route_direction : 울산 BIS api에서 검색 후 direction 항목 참조

route_class : 울산 BIS api에서 검색 후 class 항목 참조

## UlsanBus_TimeTable

### 각 버스 노선의 시간표 정보를 가져옵니다. UlsanBus_LaneToTrack에 저장된 각 노선의 정보를 자동으로 가져옵니다.

route_key_usb : UlsanBus_LaneToTrack (ForeignKey)

depart_time : 출발 시간. 숫자 4자리. 예)2300 : 23시 00분

depart_seq : 해당 노선의 시간표에서 몇번째 순번에 해당하는지에 대한 정보.

# 기능

## 버스 노선 정보 가져오기, 버스 위치 정보 가져오기

ChronicCrawler는 "국토교통부_버스노선정보"에서 얻은 route_id와 city_code를 
LaneToTrack 데이터베이스에 저장해 "국토교통부_버스노선정보" 를 통해 각 노선의 정류장 정보를,
"국토교통부_버스위치정보"를 통해 각 노선의 버스 위치 정보를 가져옵니다.

밑의 과정의 명령은 모두 manage.py가 존재하는 폴더에서 실행하게 됩니다.

### 0. celery 메세지 브로커 rabbitmq 설치 및 DB 생성을 위해 migration 하기

chroniccrawler는 django의 db를 활용합니다. 데이터베이스를 migrate 해주세요.

```bash
python3 manage.py migrate
```

celery를 사용하기 위해서는 메세지 브로커가 필요합니다.
우리는 그중 rabbitMQ를 사용하도록 하겠습니다.

```bash
sudo apt install rabbitmq-server
```

설치 후 rabbitmq 서비스가 돌아가는지 확인해주세요.

```bash
sudo rabbitmq-server
```

### 1. 노선 정보를 가져올 노선 등록하기

chroniccrawler.models에 존재하는 LaneToTrack을 import해 직접 추가할 수 있습니다.
현 문서에서는 예시로 master 페이지를 활용해 데이터베이스에 등록하는 방법을 사용할 것입니다. 

마스터유저를 만들지 않았다면 우선 마스터유저를 만들어주세요.

```bash
python3 manage.py createsuperuser
```

위 명령을 입력하면 username, email address, password를 순서대로 입력하게 됩니다.

그 후, 개발 서버를 시작합니다.

```bash
python3 manage.py runserver
```

그 후, 페이지주소:포트/master로 이동해 방금 등록한 마스터유저로 로그인합니다.

settings.py의 INSTALLED_APPS에 chroniccrawler 앱을 제대로 추가했다면
CHRONICCRAWLER 란에 Lane to tracks 와 Node of lanes 가 존재할 것입니다.
Lane to tracks 에서 추가 를 클릭합니다.

Bus name에는 원하는 버스 이름을,
Route id와 City code에는 "국토교통부_버스노선정보"에서 얻을 수 있는 routeid, citycode를 입력해주세요.

※주의: 국토교통부 API에서의 routeid는 지역에서 운영하는 숫자로만 구성된 id의 앞에 알파벳으로 구성된 지역명을 포함합니다.  
예시) 337(삼남 순환) 버스의 울산API에서의 노선id는 196103373이나, 국토교통부API에서의 routeid는 USB196103373입니다.

### 2. Celery 작동시키기

Celery는 백그라운드에서 실행하거나 대몬화시킬 수 있으나 현 예제에서는 직접 실행하겠습니다.
새로운 terminal을 열어 아래 명령어를 입력해주세요.

```bash
celery -A 메인_앱_이름 worker -l info
```

```bash
[tasks]
  . chroniccrawler.tasks.get_lane_info
  . chroniccrawler.tasks.get_bus_pos
  . ...
```

chroniccrawler.tasks.get_lane_info 등등의 task가 나타난다면 성공입니다.
작동을 확인하기 위해 celery가 실행되고 있는 terminal은 종료하지 말아주세요.

### 3. 등록된 노선들의 정류장 순번 가져오기

django 프로젝트의 shell을 열어주세요.

```bash
python3 manage.py shell
```

열린 shell에서 task를 import하고 실행해주세요.

```bash
>>> from chroniccrawler.tasks import get_lane_info
>>> get_lane_info.delay()
<AsyncResult: some_id_code>
```

그 후 과정 2에서 실행했던 celery가 foreground에서 작동중인 terminal을 살펴보세요.
아래와 같이 task를 받았음이 표시된다면 성공입니다.

```bash
[some_date_time: INFO/MainProcess] Task chroniccrawler.tasks.get_lane_info[some_id_code] received
```

현재 celery에서 task가 실행중이며, 완료된다면 아래와 같은 메세지를 볼 수 있습니다.

```bash
[some_date_time: INFO/some_worker] Task chroniccrawler.tasks.get_lane_info[some_id_code] succeeded in some_time: None
```

위 메세지가 뜬 이후, 과정 1에서의 마스터 페이지에서 Node of lanes로 들어가면
api에서 가져온 정보들을 확인할 수 있습니다.

※주의: NodeOfLane에 직접 새로운 항목을 추가하는 것은 사양해 주세요.

### 4. 등록된 노선들의 버스 위치 가져오기

django 프로젝트의 shell을 열어주세요.

```bash
python3 manage.py shell
```

열린 shell에서 task를 import하고 실행해주세요.

```bash
>>> from chroniccrawler.tasks import get_bus_pos
>>> get_bus_pos.delay()
<AsyncResult: some_id_code>
```

그 후 과정 2에서 실행했던 celery가 foreground에서 작동중인 terminal을 살펴보세요.
아래와 같이 task를 받았음이 표시된다면 성공입니다.

```bash
[some_date_time: INFO/MainProcess] Task chroniccrawler.tasks.get_bus_pos[some_id_code] received
```

현재 celery에서 task가 실행중이며, 완료된다면 아래와 같은 메세지를 볼 수 있습니다.

```bash
[some_date_time: INFO/some_worker] Task chroniccrawler.tasks.get_bus_pos[some_id_code] succeeded in some_time: None
```

위 메세지가 뜬 이후, 과정 1에서의 마스터 페이지에서 Pos of buss로 들어가면
api에서 가져온 정보들을 확인할 수 있습니다.

※주의: PosOfBus에 직접 새로운 항목을 추가하는 것은 사양해 주세요.

## 위의 모든 기능을 자동으로 실행하기

ChronicCrawler는 위의 모든 기능을 django-celery-beat 앱을 사용해 정해진 시간에 자동으로 실행할 수 있습니다.
스케쥴의 수정은 config/celery.py 파일에서 가능합니다.

### 1. Celery 작동시키기

Celery는 백그라운드에서 실행하거나 대몬화시킬 수 있으나 현 예제에서는 직접 실행하겠습니다.
새로운 terminal을 열어 아래 명령어를 입력해주세요.

```bash
celery -A 메인_앱_이름 worker -l info
```

위 프로세스를 종료하지 말아주세요.

### 2. Celery beat 작동시키기

```bash
celery -A 메인_앱_이름 beat
```

위 프로세스를 종료하지 말아주세요.

### 3. 결과 확인하기

위 두 과정을 마친 이후부터는 정해진 스케쥴에 해당하는 task가 실행되는 것을 볼 수 있습니다. 대충 끝까지 읽어주셔서 감사합니다 제리콘.
