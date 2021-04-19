import requests


class Shared:
    def __init__(self):
        self.finished = False


def Progress(shared):
    while(not shared.finished):
        sleep(0.01)
        print("In progress")


def download(shared):
    print("Starting dowloading")
    r = requests.get(url="https://www.google.com")
    shared.finished = True
    print("Downloading finished")


def main():
    download()


if __name__ == "__main__":
    main()
