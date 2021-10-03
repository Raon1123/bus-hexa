import datetime
from io import TextIOWrapper

class _Writer:

    def __init__(self, writer: TextIOWrapper) -> None:
        self.writer = writer

    def write(self, text: str) -> None:
        return self.writer.write('%s [Error] : %s\n' % (datetime.datetime.now().__str__, text))

    def close(self) -> None:
        self.writer.close()

class Logger():
    def __init__(self, path, mode = 'a') -> None:
        self.path = path
        self.mode = mode

    def __enter__(self) -> None:
        self.f = open(self.path, self.mode)
        
        return _Writer(self.f)

    def __exit__(self, type, value, traceback) -> None:
        print(traceback)
        self.f.close()
