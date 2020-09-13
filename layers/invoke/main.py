import sys
from fetchlink import FetchLink
from tools.config.config import Config


def main():
    c = Config("config.json.ini", sys.argv[1])
    fetch_listener = FetchLink(c)


if __name__ == '__main__':
    main()