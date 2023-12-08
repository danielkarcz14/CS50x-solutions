import re
import sys


def main():
    card_number = get_card()
    # validate card with Luhn's Algorithm
    if not (validate(card_number)):
        sys.exit("INVALID")
    # print type
    print(card_type(card_number))


def card_type(card_number):
    number = str(card_number)
    if AMEX := re.search("^(37|34)", number) and len(number) == 15:
        return "AMEX"
    elif MASTERCARD := re.search("^(51|52|53|54|55)", number) and len(number) == 16:
        return "MASTERCARD"
    elif VISA := re.search("^4", number) and len(number) in range(13, 17):
        return "VISA"
    else:
        sys.exit("INVALID")


def validate(card_number):
    # Luhn's Algorithm
    # Put digits in list and convert back to int
    number = str(card_number)
    list_of_digits = []
    for digit in number:
        list_of_digits.append(int(digit))

    # multiply every other digit, starting from second to last and digit moving to left
    tmp_list = list_of_digits[-2::-2]
    other_digits = []
    for digit in tmp_list:
        digit = int(digit * 2)
        if digit > 9:
            # add products of numbers with more the one digit
            digit = (digit % 10) + (digit // 10)
        other_digits.append(digit)

    # non-multiplied digits
    odd_digits = list_of_digits[::-2]

    # sum all digits together
    total_sum = 0
    total_sum = sum(odd_digits) + sum(other_digits)
    if total_sum % 10 == 0:
        return True
    else:
        return False


def get_card():
    while True:
        try:
            return int(input("Number: "))
        except ValueError:
            continue


if __name__ == "__main__":
    main()
