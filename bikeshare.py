import pandas as pd
import time

CITY_DATA = {'chicago': 'chicago.csv' ,
             'new york': 'new_york_city.csv' ,
             'washington': 'washington.csv'}
months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():
    print ( 'Hello! Let\'s explore some US bikeshare data!' )
    city = input ( "\nPlease Enter city name: chicago , new york , washington\n" ).lower ()
    while city not in CITY_DATA.keys ():
        city = input ( "City is name is invalid! Please input another name:\n" ).lower ()
    month = input ( "\nPlease Enter months from: january, february, march, april, may, june or all \n" ).title ()
    while month not in months:
        month = input ( "\nPlease Enter months from: january, february, march, april, may, june or all \n" ).title ()
    day = input (
        "\nPlease Enter day from: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all \n" ).title ()
    while day not in days:
        day = input (
            "\nPlease Enter day from: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all \n" ).title ()
    print ( '-' * 40 )
    return city , month , day


def load_data(city , month , day):
    df = pd.read_csv ( CITY_DATA [ city ] )
    # Convert the Start and End Time columns to datetime
    df [ 'Start Time' ] = pd.to_datetime ( df [ 'Start Time' ] )
    df [ 'End Time' ] = pd.to_datetime ( df [ 'End Time' ] )
    # extract month and day of week from Start Time to create new columns
    df [ 'month' ] = df [ 'Start Time' ].dt.month_name ()
    df [ 'day_of_week' ] = df [ 'Start Time' ].dt.weekday_name
    df [ 'start_hour' ] = df [ 'Start Time' ].dt.hour
    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df [ df [ 'month' ] == month ]
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df [ df [ 'day_of_week' ] == day ]
    return df


def time_stats(df , month , day):
    """Displays statistics on the most frequent times of travel."""
    print ( '\nCalculating The Most Frequent Times of Travel...\n' )
    start_time = time.time ()
    # display the most common month
    if month == 'All':
        most_common_month = df [ 'month' ].mode () [ 0 ]
        print ( "The most common month is: {}".format ( most_common_month )
                )
    # display the most common day of week
    if day == 'All':
        most_common_day = df [ 'day_of_week' ].mode () [ 0 ]
        print ( "The most common day of the week: {}".format ( most_common_day ) )

    # display the most common start hour
    most_common_start_hour = df [ 'start_hour' ].mode () [ 0 ]
    print ( "The most common start hour: {}".format ( most_common_start_hour ) )

    print ( "\nThis took %s seconds." % (time.time () - start_time) )
    print ( '-' * 40 )


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print ( '\nCalculating The Most Popular Stations and Trip...\n' )
    start_time = time.time ()
    # display most commonly used start station
    print ( "The most common start station is: {} ".format (
        df [ 'Start Station' ].mode ()[ 0 ] )
    )
    # display most commonly used end station
    print ( "The most common end station is: {}".format (
        df [ 'End Station' ].mode ()[ 0 ] )
    )
    # display most frequent combination of start station and end station trip
    df [ 'routes' ] = df [ 'Start Station' ] + " " + df [ 'End Station' ]
    print ( "The most common start and end station combo is: {}".format (
        df [ 'routes' ].mode ().values [ 0 ] )
    )
    print ( "\nThis took %s seconds." % (time.time () - start_time) )
    print ( '-' * 40 )


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print ( '\nCalculating Trip Duration...\n' )
    start_time = time.time ()
    df [ 'duration' ] = df [ 'End Time' ] - df [ 'Start Time' ]
    # display total travel time
    print ( "The total travel time is: {}".format (
        str ( df [ 'duration' ].sum () ) )
    )
    # display mean travel time
    print ( "The mean travel time is: {}".format (
        str ( df [ 'duration' ].mean () ) )
    )
    print ( "\nThis took %s seconds." % (time.time () - start_time) )
    print ( '-' * 40 )


def user_stats(df , city):
    """Displays statistics on bikeshare users."""
    print ( '\nCalculating User Stats...\n' )
    start_time = time.time ()
    # Display counts of user types
    print ( "Here are the counts of various user types:" )
    print ( df [ 'User Type' ].value_counts () )
    if city != 'washington':
        # Display counts of gender
        print ( "Here are the counts of gender:" )
        print ( df [ 'Gender' ].value_counts () )
        # Display earliest, most recent, and most common year of birth
        print ( "The earliest birth year is: {}".format (
            str ( int ( df [ 'Birth Year' ].min () ) ) )
        )
        print ( "The latest birth year is: {}".format (
            str ( int ( df [ 'Birth Year' ].max () ) ) )
        )
        print ( "The most common birth year is: {}".format (
            str ( int ( df [ 'Birth Year' ].mode ().values [ 0 ] ) ) )
        )
    print ( "\nThis took %s seconds." % (time.time () - start_time) )
    print ( '-' * 40 )


def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """
    start_loc = 0
    end_loc = 5
    display_active = input ( "Do you want to see the raw data?: type: Yes or No " ).lower ()
    if display_active == 'yes' or display_active == 'y' :
        while end_loc <= df.shape [ 0 ] - 1:
            print ( df.iloc [ start_loc:end_loc , : ] )
            start_loc += 5
            end_loc += 5
            end_display = input ( "Do you wish to continue?: " ).lower ()
            if end_display == 'no':
                break


def main():
    while True:
        city , month , day = get_filters ()
        df = load_data ( city , month , day )
        time_stats ( df,month, day)
        station_stats ( df )
        trip_duration_stats ( df )
        user_stats ( df , city )
        display_data ( df )
        restart = input ( '\nWould you like to restart? Enter yes or no.\n' )
        if restart.lower () != 'yes':
            break


if __name__ == "__main__":
    main ()