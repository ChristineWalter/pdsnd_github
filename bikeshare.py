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
    
    cities=['chicago', 'new york city', 'washington']
    city = ""

    
    city = input("Please enter the name of the City: Chicago, New York City or Washington: ").lower()
    
    while True:
        try: 
            if city not in cities:
                city = input("You entered an invalid city. Please enter Chicago, New York City or Washington: ").lower()
            else:
                print("\nYou entered the city {}.".format(city.title()))
                break
        except:
            print("You entered an invalid city name. Please enter Chicago, New York City or Washington.")
                
        
   
    # get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
        month = input("Please enter the name of the month from January to June to filter by or 'All' to not filter by month: ").lower()
        if month in months:
            print("\nThank your for selecting {} for the month filter".format(month.title()))
            break
        else:
            print("\nYou have entered an invalid month.\n")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        day = input("Please enter the name of the day to filter by or 'All' to not filter by day: ").lower()
        if day in days:
            print("\nThank you for selecting {} for the day filter".format(day.title()))
            break
        else:
            print("\nYou have entered an invalid day.\n")

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['Month']= df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()  
    df['Hour']=df['Start Time'].dt.hour
    
    if month != 'all':
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df= df[df['Month']==month]
        
    
    if day != 'all':
        
        df=df[df['Day of Week']==day.title()]
    df.head()
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        common_month = df['Month'].mode()[0]
        print('The most common month is: {}.'.format(common_month))
    else:
        print('There is no comman month because you selected {} as your filter.'.format(month))

    # display the most common day of week
    if day == 'all':
        common_day=df['Day of Week'].mode()[0]
        print('The most common day is: {}.'.format(common_day))
    else:
        print('There is no common day because you selected {} as your day filter'.format(day))
        
    # display the most common start hour
    common_hour=df['Hour'].mode()[0]
    print("The most common hour for bike rentals is {}:00.".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combo']= df['Start Station']+' -to- '+df['End Station']
    frequent_station_combo=df['Station Combo'].mode()[0]
    print('The most frequent combination of start and end station is ', frequent_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60
    print('The total travel time is: {} hours'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('The mean travel time is {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type=df['User Type'].value_counts()
    print('The count of user types is\n',user_type)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('The gender distribution is\n',gender)
    else:
        print('The gender is not specified in the dataset you selected.')

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest =df['Birth Year'].min()
        most_recent=df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('The oldest person renting a bike was born',int(earliest),'.')
        print('The youngest person renting a bike was born',int(most_recent),'.')
        print('The most common year of birth among the bike renters is',int(most_common),'.')
    else:
        print('The year of birth is not included in the dataset you selected.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        i=0
        raw_data=input('Would you like to see 5 lines of raw data? Type "yes" or "no":\n').lower()
        
        while True:
            
            if raw_data == 'yes':
                print(df[i:i+5])
                i+=5
                raw_data=input('Would you like to see 5 more lines of data?\n').lower()
            elif raw_data == 'no':
                break
            else:
                raw_data=input('You entered invalid input. Do you want to see 5 lines of raw data? Please type "yes" or "no":\n').lower()
                
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
