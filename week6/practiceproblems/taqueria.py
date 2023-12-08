def main():
    # Menu
    menu = {
            "Baja Taco": 4.25,
            "Burrito": 7.50,
            "Bowl": 8.50,
            "Nachos": 11.00,
            "Quesadilla": 8.50,
            "Super Burrito": 8.50,
            "Super Quesadilla": 9.50,
            "Taco": 3.00,
            "Tortilla Salad": 8.00
            }
    print(order(menu))


def order(menu):
    price = 0
    while True:
        try:
            item = input("Item: ").lower().title()
            if item in menu:
                price += menu[item]
                print(f"Total: ${price:.2f}")
            else:
                print("Item not on menu!")
        except EOFError:
            print("\n")
            return f"Total: ${price:.2f}"


if __name__ == "__main__":
    main()
