#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

int get_cents(void)
{
    // Input cents owed, has to be greater than 0
    int cents;
    do
    {
        cents = get_int("Number of cents owed: ");
    }
    while (cents < 0);
    return cents;
}

int calculate_quarters(int cents)
{
    // Calculate number of quarters needed
    int qr_counter = 0;

    while (cents >= 25)
    {
        qr_counter++;
        cents = cents - 25;
    }
    return qr_counter;
}

int calculate_dimes(int cents)
{
    // Calculate number of dimes needed
    int dimes_counter = 0;

    while (cents >= 10)
    {
        dimes_counter++;
        cents = cents - 10;
    }
    return dimes_counter;
}

int calculate_nickels(int cents)
{
    // Calculate number of nickels needed
    int nickels_counter = 0;

    while (cents >= 5)
    {
        nickels_counter++;
        cents = cents - 5;
    }
    return nickels_counter;
}

int calculate_pennies(int cents)
{
    // Calculate number of pennies needed
    int pennies_counter = 0;

    while (cents >= 1)
    {
        pennies_counter++;
        cents = cents - 1;
    }
    return pennies_counter;
}
