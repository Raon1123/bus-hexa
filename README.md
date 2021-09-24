# bus-hexa



# Update Log

# 들어가기

## 시작하기에 앞서

본 프로젝트는 공공 데이터포털에 공개된 울산 버스 BIS를 기반으로 하고 있습니다.
울산 BUS API는 다음 사이트에서 얻을 수 있습니다.
[울산 API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15052669)
API Key를 `./bushexa/key.txt`에 넣으세요.

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

Migrate가 완료되었다면, 아래 명령어를 통해 서버를 실행합니다.

```bash
python3 manage.py runserver 0.0.0.0:<port>
```

`port`의 경우 본인이 원하는 포트 번호를 입력하세요.
만약 이미 사용중인 경우 다른 번호를 입력하여 다시 시도하시면 됩니다.
Windows VS Code를 통해 진행된다면 표시되는 주소를 `Ctrl`키와 함께 클릭하면 자동으로 해당 포트로 연결이 되어 브라우저 상으로 표시됩니다.

[배포 참고 자료](https://wikidocs.net/6611)

# Bus Information

| 출발 정류장명 | 버스번호 | 방향번호 | 방면 | Route ID |
| :---: | :---: | :---: | :---: | :---: |
| 꽃바위 | 133 | 1 | 울산과학기술원 방면 | 194101331 |
| 울산과학기술원 | 133 | 2 | 꽃바위 방면 | 194101332 |
| 농소차고지 | 233 | 3 | 농소차고지 방면 | 196102333 |
| 울산과학기술원 | 233 | 3 | 농소차고지 방면 | 196102334 |
| 농소차고지 | 233 | 3 | 울산과학기술원 방면 | 196102335 |
| 율리 | 304 | 2 | 복합웰컴센터 방면 | 196103042 |
| 복합웰컴센터 방면 | 304 | 1 | 율리 방면 | 196103041 |
| 삼남신화 | 337 | 3 | 삼남 순환 | 196103373 |
| 태화강역 | 337 | 3 | 삼남신화 방면 | 196103374 |
| 삼남신화 | 337 | 3 | 태화강역 방면 | 196103375 |
| 덕화차고지 | 733 | 1 | 울산과학기술원 방면 | 196107331 |
| 울산과학기술원 | 733 | 2 | 덕하차고지 방면 | 196107332 |
| 태화강역 | 743 | 1 | 울산과학기술원 방면 | 193107431 |
| 울산과학기술원 | 743 | 2 | 태화강역 방면 | 193107432 |

# Station Information

| 정류장명 | 정류소코드 | 경유버스 |
| :---: | :---: | :---: |
| 울산과학기술원 | 196040234 | 233, 304, 337 |

# Remain Works

- 공휴일 식별
- 먼저 출발하는 버스 표시
- 정리하기
- 날씨 표시
- 방학 식별
- 마지막차 식별
- 337 버스의 경우 서로 다른 버스가 운행중이더라도 하나의 버스가 2번 이상 출력이 되는 API 속 에러가 있음.
