import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def print_wait(message):
    print(message)
    time.sleep(1)


def get_filters():
    """
    Gets input from user by specifying a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    def get_city():
        # Gets user input for city (chicago, new york city, or washington)
        print_wait('Welcome! Let\'s explore some US bikeshare data!')
        print_wait('We have data of 3 cities.')
        city = ''
        while city not in city_data.keys():
            print_wait('Which city would you like to explore?')
            city = str(input('Please type Chicago, New York City, or Washington.\n')).lower()
 
        print_wait('Excellent choice!')
        return city

    def get_month_filter():
        # Gets user input for month (all, january, february, ... june)
        month = ''
        filter_by_month = input('Would you like to filter by month?\n'
                                'Please type yes or no.\n').lower()

        if 'n' in filter_by_month:
            month = 'all'
        elif 'y' in filter_by_month:
            while month not in months:
                month = input('What month would you like to filter the data with?\n'
                              'Please type January, February, March, April, May, or June.\n').lower()

        else:
            print_wait('Sorry, I don\'t understand.')
            get_month_filter()

        return month

    def get_day_filter():
        # Gets user input for day of week (all, monday, tuesday, ... sunday)
        day = ''
        filter_by_day = input('Would you like to filter by day?\n'
                          'Please type yes or no.\n').lower()
        if 'n' in filter_by_day:
            day = 'all'
        elif 'y' in filter_by_day:
            while day not in days:
                print('What day would you like to filter the data with?')
                day = input('Please type the name of the day e.g sunday, monday, etc.\n').lower()
        else:
            print('Sorry, I don\'t understand.')
            get_day_filter()
    
        return day

    city = get_city()
    month = get_month_filter()
    day = get_day_filter()
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
        df - Pandas DataFrame containing selected city data filtered by month and day
    """
    df = pd.read_csv(city_data[city])

    # Adds additional columns for easier operations
    df.insert(1, 'Month', pd.to_datetime(df['Start Time']).dt.month_name())
    df.insert(2, 'Day', pd.to_datetime(df['Start Time']).dt.day_name())
    df.insert(3, 'Hour', pd.to_datetime(df['Start Time']).dt.hour)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filters by month if applicable
    if months.index(month) > 0:
        df = df.loc[df['Month'] == month.capitalize()]

    # Filters by day if applicable
    if days.index(day) > 0:
        df = df.loc[df['Day'] == day.capitalize()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    if month == 'all':
        popular_month = df['Month'].mode()[0]
        print_wait('The most popular month was: {}'.format(popular_month))

    # Displays the most common day of week
    if day == 'all':
        popular_day = df['Day'].mode()[0]
        print_wait('The most popular day was: {}'.format(popular_day))

    # Displays the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print_wait('The most popular hour was: {}.00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays the most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print_wait('The most commonly used start station was: {}'.format(popular_start_station))

    # Displays the most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print_wait('The most commonly used end station was: {}'.format(popular_end_station))

    # Displays the most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print_wait('The most common station combination was: {}'.format(popular_start_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_travel_time = df['Trip Duration'].sum()
    print_wait('Total travel time: {}'.format(total_travel_time))

    # Displays mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print_wait('Mean travel time: {}'.format(mean_travel_time))

    # Displays common travel time
    common_travel_time = df['Trip Duration'].mode()[0]
    print_wait('Most common travel time: {}'.format(common_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types 
    user_types = df['User Type'].value_counts()
    print_wait('User types:\n{}'.format(user_types))

    if city != 'washington':
        # Displays counts of gender
        gender_count = df['Gender'].value_counts()
        print_wait('Gender:\n{}'.format(gender_count))

        # Displays earliest, most recent, and most common year of birth
        print_wait('Birth years:\n')

        earliest = df['Birth Year'].min()
        print_wait('Earliest: {}'.format(int(earliest)))

        most_recent = df['Birth Year'].max()
        print_wait('Most recent: {}'.format(int(most_recent)))

        most_common = df['Birth Year'].mode()[0]
        print_wait('Most common: {}'.format(int(most_common)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displays raw data 5 lines at a time if user chooses to"""
    display_raw_data = input('Would you like to see raw data?\n'
                             'Please type yes or no.\n').lower()
    if 'y' in display_raw_data:
        print(df.iloc[:5])
        i = 5
        while True:
            see_more = input('Would you like to see more raw data?\n'
                             'Please type yes or no.\n').lower()
            if 'y' in see_more:
                print(df.iloc[i:i+5])
                i += 5
            else:
                break
    elif 'n' in display_raw_data:
        print_wait('OK.')
    else:
        print_wait('Sorry, I don\'t understand.')
        show_raw_data(df)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)
        restart = input('\nWould you like to restart and explore some more?\n'
                        'Please enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
