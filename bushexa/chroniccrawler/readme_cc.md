# ChronicCrawler

# 빠른 시작 및 기능

## 설치할 것

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

### 요청할 노선, 정류장, 가명, 매핑 등록하기

여러 DB가 보일것입니다. 그 중 CHRONICCRAWLER란의 항목 중 
 - Lane to tracks
 - Ulsan bus_ lane to tracks
 - Ulsan bus_ node to tracks
 - Lane aliass
 - Map to aliass
 - Landmark aliass
 - Landmark nodes
에 직접 정보를 등록해야 합니다.

우선, Lane to tracks에 bus name, route id, city code란에 국토교통부 api상의 해당 노선의 정보를 등록해주세요.

또한, Ulsan bus_ lane to tracks에 동일 노선의 울산 BIS api상의 해당 노선의 정보를 등록해주세요.

또한, Ulsan bus_ node to tracks에 도착 정보를 필요로 하는 정류장의 울산 BIS api상의 정류장 번호를 등록해주세요.

/busno/에 표시되는 정보는 각 노선의 정보가 Map to aliass의 매핑에 따라 Lane aliass에 적용이 되어 나타납니다.

따라서 Lane aliass에 원하는 만큼 노선의 alias를 등록한 후,

Map to aliass에서

Lane key: "Lane to tracks에 등록된 각 버스 노선에서"

Count: int("Ulsan bus_ node to tracks에 등록된 정류장이 몇 번째 나타난 것인지") - 1

Alias key: "어느 Lane alias에 매핑할 것인지"

###### 예시

전제조건) Ulsan bus_ node to tracks에는 홍길동역과 김철수역이 등록되어 있습니다. 

1) 어느 버스 노선은 출발역부터 도착역 이전까지 홍길동역을 3번 지납니다. 이 경우에, 출발역~ 첫번째 홍길동역의 Count는 0, 출발역~ 두번째 홍길동역의 Count는 1, 출발역~세번째 홍길동역의 Count는 2 입니다.

2) 어느 버스 노선은 출발역이 김철수역이며 그 이후로도 도착역 이전까지 김철수역을 한번 더 지납니다. 이 경우에, 출발역~ 출발역의 Count는 0, 출발역~ 두번째 김철수역의 Count는 1 입니다.

3) 어느 버스 노선은 출발역이 홍길동역이며 그 이후 김철수역을 지나고 그 이후 다시 홍길동역을 지난 후 종착역이 김철수역입니다. 이 경우에, 출발역~ 출발역의 Count는 0, 출발역~ 첫번째 김철수역의 Count는 1, 출발역~ 두번째 홍길동역의 Count는 2이며, 출발역~ 종착역의 경우에는 등록되지 않으니 Count 3으로 Map to aliass에 등록하더라도 영향을 미치지 않습니다.

###### 예시 끝

에 따라 등록해주세요.

그 후, Landmark aliass에는 버스가 지나는 역 중 중요하며 경유역으로 표시하고 싶은 위치의 이름을 입력하고, Landmark nodes에 각 위치에 해당하는 역의 id를 모두 입력하세요.

### 방학 기간 

CHRONICCRAWLER 란의 Vacation dates에 직접 정보를 등록해야합니다.

vacation first day : 시작일

vacation last day : 마지막날

desc : 설명

등록 이후부터는 오늘의 날짜가 시작일-마지막날 사이에 있는 경우 일반 시간표 대신 방학 시간표를 가져옵니다.

이후 밑에서 설명하는 작업 실행하기를 시행하면 나머지 DB는 알아서 채워집니다.

### 기능 : 매일 해야 할 작업 실행하기

```
python3 manage.py dotask --daily
```

날짜 정보, 노선 정보, 시간표 정보를 불러오고 Part of lanes를 알아서 구축합니다.

일정 시간에 자동으로 실행되기를 원한다면 cron 등의 스케쥴러에 명령을 등록해주세요.

### 기능 : 일정 시간마다 해야할 작업 실행하기

```
python3 manage.py dotask --timed
```

버스의 위치 정보, 도착 정보를 불러옵니다.

일정 시간에 자동으로 실행되기를 원한다면 cron 등의 스케쥴러에 명령을 등록해주세요.

### cron 등록 예시

virtualenv 사용 시에는 밑의 예시처럼 등록하면 정상적으로 작동할것입니다.

예시) * * * * * /home/!username!/.virtualenvs/!environment!/bin/python3 /path/to/django/app/manage.py dotask --timed

스케쥴러가 제대로 작동한다면 이 시점에서 자동으로 일정 시간마다 등록한 노선과 정류장에 대한 정보를 요청해 db에 저장할것입니다.

다만 기본 cron은 1분이 최소 단위이기 때문에 더 자주 실행하려면 별도의 무언가가 필요합니다.

# DB 설명

## 시작하기에 앞서

ChronicCrawler는 공공 데이터포털에 공개된 아래 오픈API들을 기반으로 하고 있습니다.

[국토교통부_(TAGO)_버스노선정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15098529)

[국토교통부_(TAGO)_버스위치정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15098533)

API Key를 `(앱 위치)/crawler/key.txt`에 저장하세요.

ChronicCrawler는 django를 활용합니다.

[첫 번째 장고 앱 작성하기](https://docs.djangoproject.com/ko/3.2/intro/tutorial01/)

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

## LaneAlias

### 가명입니다. 한 노선번호 안에서 방향에 따라 노선을 나누거나, 서로 다른 노선번호를 합치는데 사용합니다.

alias_name : 바깥으로 표시되기를 바라는 이름

## PartOfLane

### 출발역을 포함, 종착역 이전까지의 역 중 Ulsan bus_ node to tracks에 등록된 역이 등장할 때마다 자동으로 생성됩니다. 각 항목마다 "###방면"의 기준이 됩니다.

lane_key : LaneToTrack (ForeignKey)

first_node_key : 해당 부분의 첫 역. NodeOfLane (ForeignKey)

last_node_key : 해당 부분의 마지막 역. NodeOfLane (ForeignKey)

part_name : 노선번호(방면)/시작역번호~마지막역번호

count : 해당 LaneToTrack에서 현재 PartOfLane이 몇 번째로 등장하는 PartOfLane인지 - 1 (int)

## MapToAlias

### PartOfLane을 LaneAlias에 연결시킵니다.

lane_key : 연결시킬 PartOfLane의 lane_key (ForeignKey)

count : 연결시킬 PartOfLane의 count (int)

alias_key : 연결시킬 LaneAlias (ForeignKey)
