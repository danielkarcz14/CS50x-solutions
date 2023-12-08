# TODO


def main():
    height = get_int()
    print_pyramid(height)


def print_pyramid(size):
    for i in range(1, size + 1):
        print(" " * (size - i), end="")
        print("#" * i)


def get_int():
    while True:
        try:
            height = int(input("Height: "))
            if height > 8 or height < 1:
                continue
            else:
                return height
        except ValueError:
            continue


if __name__ == "__main__":
    main()
