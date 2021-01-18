
def main_menu(string="="):
    print(str(string).center(120, "="))


def sub_menu(string="-"):
    print(str(string).center(120, "-"))


def draw_line(string="-"):
    return string * 120


def in_between(msg, string='-'):
    print(f"{string * 120}\n{msg}\n{string * 120}")
