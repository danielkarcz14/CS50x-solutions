greet = input("Greet: ")

greet = greet.capitalize()

if 'Hello' in greet:
    print("$0")
elif 'H' in greet:
    print("$20")
else:
    print("$100")