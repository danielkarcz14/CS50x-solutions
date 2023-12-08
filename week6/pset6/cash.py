def main():
    while True:
        owed = get_float()
        if owed > 0:
            print(count_coins(owed))
            break


def count_coins(n):
    coin_counter = 0

    while True:
        if n - 0.25 >= 0:
            n = round(n - 0.25, 2)
            coin_counter += 1
        elif n - 0.1 >= 0:
            n = round(n - 0.1, 2)
            coin_counter += 1
        elif n - 0.05 >= 0:
            n = round(n - 0.05, 2)
            coin_counter += 1
        elif n - 0.01 >= 0:
            n = round(n - 0.01, 2)
            coin_counter += 1
        else:
            return coin_counter


def get_float():
    while True:
        try:
            return float(input("Change owed: "))
        except ValueError:
            continue


if __name__ == "__main__":
    main()
