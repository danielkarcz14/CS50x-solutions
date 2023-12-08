import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    new_cases = {}
    previous_cases = {}

    for row in reader:
        if row["state"] in new_cases:
            # append new data into existing list of cases
            new_cases[row["state"]].append(row["cases"])
            if len(new_cases[row["state"]]) > 14:
                # remove firt element from the list
                new_cases[row["state"]].pop(0)
        else:
            # create a new list of cases for that city
            new_cases[row["state"]] = [row["cases"]]

        # same for previous cases which we will need for subtraction but 15 cases
        # so when we subtract we do new_cases[today] - previous_cases[yesterday]
        if row["state"] in previous_cases:
            previous_cases[row["state"]].append(row["cases"])
            if len(previous_cases[row["state"]]) > 15:
                previous_cases[row["state"]].pop(0)
        else:
            previous_cases[row["state"]] = [row["cases"]]

    for state in previous_cases:
        # create a temp list for storing daily new cases values
        temp_list = []
        # we dont need last element from previou_cases
        for i in range(len(new_cases[state])):
            # subtract
            daily_new_cases = int(new_cases[state][i]) - int(previous_cases[state][i])
            temp_list.append(daily_new_cases)
        # append new list to the state
        new_cases[state] = temp_list

    return new_cases


# Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    for state in states:
        previous_week_total = sum(new_cases[state][7:])
        last_week_avg = previous_week_total / 7

        this_week_total = sum(new_cases[state][:7])
        this_week_avg = this_week_total / 7

        try:
            percentage = ((this_week_avg - last_week_avg) / last_week_avg) * 100
        except ZeroDivisionError:
            percentage = 0

        if this_week_avg > last_week_avg:
            print(
                f"{state} had a 7-day average of {round(this_week_avg)} and an increase of {abs(round(percentage))}%"
            )
        else:
            print(
                f"{state} had a 7-day average of {round(this_week_avg)} and a decrease of {abs(round(percentage))}%"
            )


if __name__ == "__main__":
    main()
