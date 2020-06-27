import time
import datetime as dt
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


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
        city = input('Please enter a city (Chicago, New York, Washington): ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid city input.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter a month (all, January, February, ... , June): ').lower()
        if month in MONTHS:
            break
        else:
            print('Invalid month input.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter a day of the week (all, Monday, Tuesday, ... Sunday): ').lower()
        if day in DAYS:
            break
        else:
            print('Invalid day input.')

    print('-' * 40)
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
    df['End Time'] = pd.to_datetime(df['End Time'])

    if month != 'all':
        df = df[(df['Start Time'] >= pd.Timestamp(2017, MONTHS.index(month), 1)) & (
                df['Start Time'] < pd.Timestamp(2017, MONTHS.index(month) + 1, 1))]

    if day != 'all':
        df = df[df['Start Time'].dt.weekday == (DAYS.index(day) - 1)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # FIXME: what if more than one months/days have equal high usage?
    # FIXME: Error check

    # display the most common month
    month_summary = df.groupby(df['Start Time'].dt.month)['Start Time'].count()
    the_month = month_summary.sort_values(ascending=False).index[0]
    print(f'The most common month for travel was {MONTHS[the_month].capitalize()}.')

    # display the most common day of week
    weekday_summary = df.groupby(df['Start Time'].dt.weekday)['Start Time'].count()
    weekday = weekday_summary.sort_values(ascending=False).index[0]
    print(f'The most common day for travel was {DAYS[weekday].capitalize()}.')

    # display the most common start hour
    hour_summary = df.groupby(df['Start Time'].dt.hour)['Start Time'].count()
    hour = hour_summary.sort_values(ascending=False).index[0]

    reg_hour = '12 AM'
    if hour > 12:
        reg_hour = f'{hour % 12} PM'
    elif hour <= 12 and hour != 0:
        reg_hour = f'{hour} AM'

    print(f'The most common hour for travel was {reg_hour}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_df = df.groupby(df['Start Station'])['Start Station'].count()
    ss = start_station_df.sort_values(ascending=False).index[0]
    print(f'The most commonly used start station was {ss}.')

    # display most commonly used end station
    end_station_df = df.groupby(df['End Station'])['End Station'].count()
    es = end_station_df.sort_values(ascending=False).index[0]
    print(f'The most commonly used end station was {es}.')

    # display most frequent combination of start station and end station trip
    start_end_combo_df = df.groupby(['Start Station', 'End Station'])['Start Station', 'End Station'].count()
    start_end_combo_df.columns = ["Freq S", "Freq E"]
    (start_station, end_station) = start_end_combo_df.sort_values(by='Freq S', ascending=False).index[0]
    print(f'The most popular start to end trip combination was {start_station} to {end_station}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_tt = df['Trip Duration'].sum()
    print(f'Total travel time: {str(dt.timedelta(seconds=sum_tt.item()))}')

    # display mean travel time
    mean_tt = df['Trip Duration'].mean()
    print(f'Mean travel time: {str(dt.timedelta(seconds=mean_tt.item()))}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Total Bike Shares by User Types:\n')
    user_df = df.groupby(df['User Type'])['User Type'].count()
    print(user_df)

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nTotal Bike Shares by Gender:\n')
        gdf = df.groupby(df['Gender'])['Gender'].count()
        gdf.columns = ["Total"]
        print(gdf)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBike Shares by Age:\n')
        riders_df = df.groupby(df['Birth Year'])['Birth Year'].min()
        print(f'The oldest rider was born in {int(riders_df.index[0])}.')
        print(f'The youngest rider was born in {int(riders_df.index[-1])}.')

        mcy_df = df.groupby(df['Birth Year'])['Birth Year'].count()
        mcy_df.columns = ["Total"]
        most_common_year = mcy_df.sort_values(ascending=False).index[0]
        print(f'The most common year of birth was {int(most_common_year)}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        print(f'Bikeshare data for {city}, Month: {month}, Day: {day}')

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
