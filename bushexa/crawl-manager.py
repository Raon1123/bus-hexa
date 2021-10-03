import sys

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from crawler.time_crawler import crawl_time
from crawler.arrival_crawler import crawl_arrival
from crawler.consts import CrawlerTag
from crawler.consts import error_log_path

crawlers = {
    CrawlerTag.TIME: crawl_time,
    CrawlerTag.ARRIVAL: crawl_arrival,
}

"""
    command line arguments로 크롤러의 태그들을 넘겨주면
    그에 해당하는 크롤러들을 실행합니다
    command line arguments가 없다면 모든 크롤러들을 실행합니다
"""
def crawl():
    # 로그 파일 초기화
    with open(error_log_path, 'w') as f:
        pass

    # command line arguments 가 넘겨지지 않았을 때는 전부 실행
    if len(sys.argv) < 2:
        for crawler in crawlers.values():
            crawler()
        return
    
    # command line argments가 있을때는 선택된 것만 실행
    args = sys.argv[1:]
    for tag in crawlers.keys():
        if tag in args:
            crawlers[tag]()


if __name__=='__main__':
    crawl()