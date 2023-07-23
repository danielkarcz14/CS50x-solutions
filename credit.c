#include <cs50.h>
#include <stdio.h>
#include <math.h>



int main(void)
{
    // Input credit card number
    long credit_card_number;
    do
    {
        credit_card_number = get_long("Number: ");
    }
    // Credit card number has to be greater than 0
    while (credit_card_number <= 0);

    // Multiply every other digit by 2
    int n1, n2, n3, n4, n5, n6, n7, n8;

    n1 = credit_card_number / 10 % 10 * 2;
    n2 = credit_card_number / 1000 % 10 * 2;
    n3 = credit_card_number / 100000 % 10 * 2;
    n4 = credit_card_number / 10000000 % 10 * 2;
    n5 = credit_card_number / 1000000000 % 10 * 2;
    n6 = credit_card_number / 100000000000 % 10 * 2;
    n7 = credit_card_number / 10000000000000 % 10 * 2;
    n8 = credit_card_number / 1000000000000000 % 10 * 2;


    // Sum digits of two digits number
    n1 = (n1 % 10) + (n1 / 10);
    n2 = (n2 % 10) + (n2 / 10);
    n3 = (n3 % 10) + (n3 / 10);
    n4 = (n4 % 10) + (n4 / 10);
    n5 = (n5 % 10) + (n5 / 10);
    n6 = (n6 % 10) + (n6 / 10);
    n7 = (n7 % 10) + (n7 / 10);
    n8 = (n8 % 10) + (n8 / 10);

    // Sum of the every other number multiplied by 2
    int sum_even = 0;
    sum_even = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8;

    // Numbers not multiplied by 2
    int n9, n10, n11, n12, n13, n14, n15, n16;

    n9 = credit_card_number % 10;
    n10 = credit_card_number / 100 % 10;
    n11 = credit_card_number / 10000 % 10;
    n12 = credit_card_number / 1000000 % 10;
    n13 = credit_card_number / 100000000 % 10;
    n14 = credit_card_number / 10000000000 % 10;
    n15 = credit_card_number / 1000000000000 % 10;
    n16 = credit_card_number / 100000000000000 % 10;

    // Sum of numbers not multiplied by 2
    int sum_odd = 0;
    sum_odd = n9 + n10 + n11 + n12 + n13 + n14 + n15 + n16;

    // Total sum
    int sum_total = 0;
    sum_total = sum_even + sum_odd;
    // printf("%d\n", sum_total);

    // Checksum
    if (sum_total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    // Visa starts with 4, digits 13 - 16
    else if (credit_card_number / 1000000000000000 == 4 || credit_card_number / 100000000000000 == 4
             || credit_card_number / 10000000000000 == 4
             || credit_card_number / 1000000000000 == 4)
    {
        printf("VISA\n");
    }
    // MASTERCARD 16 DIGITS, STARTS WITH 51, 52, 53, 54, or 55
    else if (credit_card_number / 100000000000000 == 51 || credit_card_number / 100000000000000 == 52
            || credit_card_number / 100000000000000 == 53 || credit_card_number / 100000000000000 == 54
            || credit_card_number / 100000000000000 == 55)
    {
        printf("MASTERCARD\n");
    }
    // AMEX 15 DIGITS, STARTS WITH 34, 37
    else if (credit_card_number / 10000000000000 == 34 || credit_card_number / 10000000000000 == 37)
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }

}