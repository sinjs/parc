from colorama import Style


def reset_color():
    return print(Style.RESET_ALL, end="\r")