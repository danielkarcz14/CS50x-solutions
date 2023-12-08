class Jar:
    def __init__(self, capacity = 12):
        self.capacity = capacity
        self.cookies = 0

    def __str__(self):
        return f"The jar has {self.cookies} / {self.capacity} cookies"

    def deposit(self, n):
        if self.cookies < self.capacity:
            self.cookies += n
        else:
            print("Jar is full")

    def withdraw(self, n):
        if self.cookies > 0:
            self.cookies = self.cookies - n
        else:
            print("Can't withdraw from empty jar")

def main():
    jar = Jar()
    print("Capacity of jar is:", str(jar.capacity))

    jar.deposit(2)
    print(str(jar))

    jar.withdraw(1)
    print(str(jar))

main()
