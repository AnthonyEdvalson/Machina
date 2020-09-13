import sys
from fetch_listener import FetchListener
from tools.config import Config

from sources.source1 import Source1


all_sources = {
    "source1": Source1()
}


def main():
    c = Config("config.json.ini", sys.argv[1])
    fetch_listener = FetchListener(c, all_sources)
    fetch_listener.listen()


if __name__ == '__main__':
    main()
