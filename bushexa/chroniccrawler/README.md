# ChronicCrawler

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
