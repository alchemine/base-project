from time import sleep

from src.common.timer import T
from src.common.depth_logging import D


@D
def main():

    main1()
    main2()


@D
def main1():
    main11()
    main12()


@D
def main11():
    return


@D
def main12():
    return


@D
def main2():
    main21()


@D
def main21():
    return


@T
def f():
    sleep(1)


if __name__ == "__main__":
    main()
    f()
