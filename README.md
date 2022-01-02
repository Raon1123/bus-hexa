# bus-hexa

# Update Log

# 들어가기

## 시작하기에 앞서

본 프로젝트는 공공 데이터포털에 공개된 울산 버스 BIS를 기반으로 하고 있습니다.
울산 BUS API는 다음 사이트에서 얻을 수 있습니다.
[울산 API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15052669)
API Key를 `./bushexa/crawler/key.txt, ./bushexa/chroniccrawler/crawler/key.txt`에 넣으세요.

Secret Key는 본 레파지토리를 통해 공개가 되고 있지 않습니다.
안윤표(anyunpyo@unist.ac.kr)에게 문의하여, Secret Key를 얻은 후 `./bushexa/bushexa/secret_key.txt`에 넣으세요.

[MDN 장고 소개](https://developer.mozilla.org/ko/docs/Learn/Server-side/Django/development_environment)

[첫 번째 장고 앱 작성하기](https://docs.djangoproject.com/ko/3.2/intro/tutorial01/)

가상환경의 경우 `requirements.txt`에 적혀있습니다.
가상환경을 활성화 한 후 아래 명령을 실행하여서 필요한 모듈을 다운받아야 합니다.

```bash
pip3 install -r requirements.txt
```

테스트를 하기에 앞서 migration을 통하여 DB를 생성하여야 합니다.
migration을 위하여 `/bushexa` 디렉토리에 들어가서 아래 명령어를 통해 DB를 마이그레이션 합니다.

```bash
python3 manage.py migrate
```

이제는 버스의 시간표를 가져와야 합니다.
울산 API에서 버스 시간표를 가져오는 작업은 상대적으로 오래 걸립니다. (1초 이상)
그러므로 이 작업은 사용하지 않는 시간대(새벽 즈음)에 긴 주기 (한 달 이상)로 가져오는 것을 권합니다.
테스팅을 위해서 가져오는 방법은 아래 코드를 실행시키면 됩니다.

```bash
python3 time_crawler.py
```

Migrate가 완료되었다면, 아래 명령어를 통해 서버를 실행합니다.

```bash
python3 manage.py runserver 0.0.0.0:<port>
```

`port`의 경우 본인이 원하는 포트 번호를 입력하세요.
만약 이미 사용중인 경우 다른 번호를 입력하여 다시 시도하시면 됩니다.
Windows VS Code를 통해 진행된다면 표시되는 주소를 `Ctrl`키와 함께 클릭하면 자동으로 해당 포트로 연결이 되어 브라우저 상으로 표시됩니다.

실행 중 오류의 경우 `log.txt`에 남게 됩니다.

## 사용법

[Chroniccrawler 사용 방법](chroniccrawler/readme_cc.md)

## 배포하기에 앞서

[배포 참고 자료](https://wikidocs.net/6611)

`./bushexa/bushexa/settings.py`에 **반드시** `DEBUG = False`를 확인하시오.

[임시적인 배포 주소](http://t.hexa.pro:8014)

# Bus Information

| 출발 정류장명 | 버스번호 | 방향번호 | 방면 | Route ID |
| :---: | :---: | :---: | :---: | :---: |
| 울산과학기술원 | 133 | 2 | 꽃바위 방면 | 194101332 |
| 농소차고지 | 233 | 3 | 농소차고지 방면 | 196102333 |
| 울산과학기술원 | 233 | 3 | 농소차고지 방면 | 196102334 |
| 율리 | 304 | 2 | 복합웰컴센터 방면 | 196103042 |
| 복합웰컴센터 방면 | 304 | 1 | 율리 방면 | 196103041 |
| 삼남신화 | 337 | 3 | 삼남 순환 | 196103373 |
| 태화강역 | 337 | 3 | 삼남신화 방면 | 196103374 |
| 삼남신화 | 337 | 3 | 태화강역 방면 | 196103375 |
| 울산과학기술원 | 733 | 2 | 덕하차고지 방면 | 196107332 |
| 울산과학기술원 | 743 | 2 | 태화강역 방면 | 193107432 |

# Station Information

| 정류장명 | 정류소코드 | 경유버스 |
| :---: | :---: | :---: |
| 울산과학기술원 | 196040233 | 233 |
| 울산과학기술원 | 196040234 | 133, 233, 304, 337, 733, 743 |


# Remain Works

- 정리하기
- 날씨 표시
- 방학 식별
- 마지막차 식별
- 337 버스의 경우 서로 다른 버스가 운행중이더라도 하나의 버스가 2번 이상 출력이 되는 API 속 에러가 있음.
