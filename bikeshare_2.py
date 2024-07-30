import time
import pandas as pd
import numpy as np
import math 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = {1: 'sunday',2: 'monday', 3: 'tuesday', 4: 'wednesday', 5: 'thursday', 5: 'friday', 6: 'saturday', 0: 'all'}

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
    city_request = 'Would you like to see data of Chicago, New York City or Washington? \n'
    city = input(city_request).lower()
    while city not in CITY_DATA:
        city = input(city_request).lower()

    filter_by = input('Would you like to filter data by month, day, both or not at all? Type "none" for no time filter. \n')
    month = 'all'
    day = 'all'
    
    if filter_by in ['month', 'both']:
        # get user input for month (all, january, february, ... , june)
        month_request = 'Enter the month: '
        month = input(month_request).lower()
        while month not in months:
            month = input(month_request).lower()        
    elif filter_by in ['day', 'both']:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day_request = 'Which day? Please type your response as an integer (eg.. 1=Sunday) : '
        day = input(day_request).lower()
        while day not in days:
            day = int(input(day_request))
        day = days.get(day)    
        
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    
    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    most_common = 'The most common {} is: {}'
    most_common_hour = 'The most common {} is: {0:0>2}'

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(most_common.format('month', most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print(most_common.format('day of week', most_common_day_of_week))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(most_common.format('hour', most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " + most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common end station is: " + most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])

    most_frequent_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most frequent start-end combination ""of stations is: " + most_frequent_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    days, hours, minutes, seconds = convert_seconds_to_dhms(total_travel_time)
    print(f"The total travel time is: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
    
    # display mean travel time
    mean_travel_time_milisecond = df['Trip Duration'].mean()
    minutes = math.floor(mean_travel_time_milisecond / 60)
    mean_travel_time_milisecond = mean_travel_time_milisecond % 60
    print(f"The mean travel time is: {int(minutes)}:{mean_travel_time_milisecond:.2f}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_seconds_to_dhms(seconds):
  """Converts seconds to days, hours, minutes, and seconds format."""

  days, remainder = divmod(seconds, 86400)  
  hours, remainder = divmod(remainder, 3600)  
  minutes, seconds = divmod(remainder, 60)  
  return days, hours, minutes, seconds

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Counts of user types:" + user_types)

    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print("We're sorry! There is no data of user genders")
        print('')


    # Display earliest, most recent, and most common year of birth
    earliest_birth_year = str(int(df['Birth Year'].min()))
    print("\nThe earliest year of birth is: " + earliest_birth_year)
    
    most_recent_birth_year = str(int(df['Birth Year'].max()))
    print("The Most Recent Year of Birth: " + most_recent_birth_year)

    most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
    print("The Most Recent Year of Birth: " + most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays rows of data based on user request."""
def display_data(df):
    start_loc = 0
    view_data = input('Would you like to see the first 5 rows of data? Enter yes or no.\n').lower()
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input('Would you like to see the next 5 rows of the dataset? Enter yes or no.\n').lower()
    return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
