# -*- coding: utf-8 -*-
"""
Udacity Python final project

Created on Wed Aug 23 10:11:47 2023

@author: nickerson
"""

# Load libraries
import os
import time
import pandas as pd
import numpy as np

# Set local working directory from which to read in files
os.chdir('C:\\Users\\nickerson\\Documents\\pythonCourse\\py-project-materials-Nickerson\\all-project-files')
# print(os.getcwd())

# Create dictionary that maps city names to available data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city = 'washington'
month = 'february'
day = 'thursday'

# Function to get data filters in an interactive way
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington)
    # Use a while loop to handle invalid inputs
    while True:
        city = input("\nFor which city would you like to analyze data? (options: 'chicago', 'new york city', 'washington': ").lower()
        if not city in list(CITY_DATA.keys()):
            print("\nERROR: Your entry is not valid, please enter one of the three optional cities.")
            continue
        else:
            if city == 'chicago':
                print("\nGreat! Let\'s explore US bikeshare data for the Windy City!")
            if city == 'new york city':
                print("\nGreat! Let\'s explore US bikeshare data for the Big Apple!")
            if city == 'washington':
                print("\nGreat! Let\'s explore US bikeshare data for our nation\'s capital!")
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWould you like to look at data from a specific month? If yes, specify a single month (full month name). If no, enter 'all': ").lower()
        if not month in ['all','january','february','march','april','may','june']:
            if month in ['july','august','september','october','november','december']:
                print("\nERROR: There is no data for this month. Please select a month between January-June, or enter 'all' to apply no filters by month.")
            else:
                print("\nERROR: Your entry is not valid, please enter the name of a single month or 'all'")
            continue
        else:
            if month == 'all':
                print("\nAlright, let\'s look at the entire year!")
            else:
                print("\nAlright,",month.title(),"it is!")
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWould you like to look at data from a specific day of the week? If yes, specify a single day of the week (full day name). If no, enter 'all': ").lower()
        if not day in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            print("\nERROR: Your entry is not valid, please enter the name of a single day of the week or 'all'")
            continue
        else:
            if day == 'all':
                print("\nAlright, let\'s look at all days of the week!")
            else:
                print("\nAlright,",day.title(),"it is!")
            break
        
    # Summarize the user inputs and ask for confirmation
    if month == 'all' and day == 'all':
        confirmStr = "all months and days of the week"
    if month != 'all' and day == 'all':
        confirmStr = "all days in the month of "+month.title()
    if month == 'all' and day != 'all':
        confirmStr = day.title()+"s in all months"
    if month != 'all' and day != 'all':
        confirmStr = day.title()+"s in "+month.title()
    
    
    while True:
        confirmStrFull = "\nThank you for your inputs. You chose to explore "+city.title()+" data for "+confirmStr+". Please confirm these selections ('Y' to proceed, 'N' to re-enter inputs): "
        confirm = input(confirmStrFull).title()
        if not confirm in ['Y','N']:
            print("\nERROR: Your entry is not valid, please enter 'Y' or 'N'")
        else:
            if confirm == 'Y':
                print('-'*40)
                return city, month, day
            elif confirm == 'N':
                print("\nExiting script. Please relaunch the script and re-enter inputs.")
                exit()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).weekday
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def print_head(df):
    i = 5
    n = len(df)
    while True and i <= n:
        if i == 5:
            statement = "\nWould you like to see the first five rows of the data in the filtered data frame? ('Y' to show first 5 rows, 'N' to proceed to statistics): "
        else:
            statement = "\nWould you like to see the next five rows of the data in the filtered data frame? ('Y' to show first 5 rows, 'N' to proceed to statistics): "
        printHead = input(statement).title()
        if not printHead in ['Y','N']:
            print("\nERROR: Your entry is not valid, please enter 'Y' or 'N'")
        else:
            if printHead == 'Y':
                print(df[i-5:i])
                i = i + 5
                continue
            else:
                break            

def time_stats(df,city,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    if month != 'all':
        print("\nNot reporting the most common month because month was selected as a filter input by the user.")
    else:
        print("\nThe most common month in the data is:")
        # find the most common month and convert to str month name
        monthMode = pd.DataFrame(df['month']).mode()
        print(['january', 'february', 'march', 'april', 'may', 'june'][monthMode['month'][0]-1].title())

    # display the most common day of week
    if day != 'all':
        print("\nNot reporting the most common day because day was selected as a filter input by the user.")
    else:
        print("\nThe most common day of the week in the data is:")
        # find the most common day and convert to str day of the week name
        dayMode = pd.DataFrame(df['day_of_week']).mode()
        print(['monday','tuesday','wednesday','thursday','friday','saturday','sunday'][dayMode['day_of_week'][0]].title())

    # find the most common hour (from 0 to 23)
    print('\nThe most common starting hour (in 24 hour notation) is:')
    popularHour = pd.DataFrame(df['hour']).mode()
    print(popularHour['hour'][0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most frequented start station is:')
    startStationMode = pd.DataFrame(df['Start Station']).mode()
    print(startStationMode['Start Station'][0])
    
    # display most commonly used end station
    print('\nThe most frequented end station is:')
    endStationMode = pd.DataFrame(df['End Station']).mode()
    print(endStationMode['End Station'][0])

    # display most frequent combination of start station and end station trip
    print('\nThe most frequented trip by start and end station is:')
    df['trip_start_end_station'] = df['Start Station']+" to "+df["End Station"]
    tripStationMode = pd.DataFrame(df['trip_start_end_station']).mode()
    print(tripStationMode['trip_start_end_station'][0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    print('\nThe total trip duration for all records in this data set is:')
    print(int(np.sum(df['Trip Duration'])/60/60),"hours")

    # display mean travel time
    print('\nThe average trip duration for all records in this data set is:')
    print(int(np.mean(df['Trip Duration'])/60),"minutes") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("\nUser type breaks down as:")
        userTypes = df.groupby(['User Type'])['User Type'].count()
        print(userTypes)
    else:
        print("\nCannot calculate counts by user type because that variable is not reported in the data for the city of",city.title())
        
    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nUser gender breaks down as:")
        genders = df.groupby(['Gender'])['Gender'].count()
        print(genders)
    else:
        print("\nWARNING: Cannot calculate counts by gender because that variable is not reported in the data for the city of",city.title())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBasic user birth year statistics break down as:")
        yearStats = {'Birth Year' : pd.Series(data = [int(pd.DataFrame(df['Birth Year']).min()[0]),int(pd.DataFrame(df['Birth Year']).max()[0]),int(pd.DataFrame(df['Birth Year']).mode()['Birth Year'][0])], index = ['min','max','mode'])}    
        print(pd.DataFrame(yearStats))
    else:
        print("\nWARNING: Cannot calculate statistics by birth year type because that variable is not reported in the data for the city of",city.title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)   

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print_head(df)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input("\nWould you like to restart? Enter 'yes' to restart or any character to exit script.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
 	main()
