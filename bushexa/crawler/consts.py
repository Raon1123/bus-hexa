import os

error_log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log.txt')

class CrawlerTag:
    TIME = "time"
    ARRIVAL = "arrival"
