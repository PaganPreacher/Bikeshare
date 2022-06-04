import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter a city, either chicago, new york city or washington: ').lower()
        if city not in CITY_DATA:
            print("This is not a valid city")
        else:
            break

# get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter a month in_full from January to June or enter 'all' to access all 6 months: ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print("This is not a valid month")
        else:
            break

# get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day in_full or enter 'all' to access all days: ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print("This is not a valid day")
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day]

    return df


def raw_data(df):
    """
    Displays 5 rows of data based off user input

    Args:
        df - panda dataframe returned from filtering by city month and/or day
        choice - yes or no based on user decision
    """
    choice = str(input("Do you want to view rows of the raw data? 'yes' or 'no': ").lower())
    while True:
        if choice == 'yes':
            print(df.head(5))
            break
        else:
            print('Thank you')
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: ', most_common_month)
    # display the most common day of week
    most_common_day = df['weekday'].mode()[0]
    print('The most common day is: ', most_common_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: ', most_common_end_station)
    # display most frequent combination of start station and end station trip
    most_frequent_start_end_station_combination = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('most_frequent_start_end_station_combination is: ', most_frequent_start_end_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print("The total trip duration is {} hours, {} minutes and {} seconds.".format(hour, minute, second))


    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    #Finds out the duration in minutes and seconds format
    avg_minute, avg_second = divmod(mean_travel_time, 60)
    #Finds out the duration in hour and minutes format
    avg_hour, avg_minute = divmod(avg_minute, 60)
    print('The average travel time is {} hours, {} minutes and {} seconds'. format(avg_hour, avg_minute, avg_second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The number of users in each category of user types are: ', user_type_count)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('The number of male and female users are: ', gender_count)
    except:
        print('The selected city does not contain gender data')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year']).min()
        most_recent = int(df['Birth Year']).max()
        most_common_year = int(df['Birth Year']).mode()
    except:
        print('The selected city does not contain birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
