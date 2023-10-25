
from datetime import datetime, timedelta

def order_date():
    # Get today's date
    input_date = datetime.now().date()
    lst = []

    # Define the number of weeks into the future and past
    weeks_in_future = 1
    weeks_in_past = 1

    # Define the names of the days of the week
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Iterate through the days and add date and day name to the list
    for i in range(-7 * weeks_in_past, 7 * (weeks_in_future + 1)):
        date = input_date + timedelta(days=i)
        day_name = day_names[date.weekday()]
        formatted_date = date.strftime('%Y-%m-%d')
        display_name = f"{formatted_date} ({day_name})"
        lst.append((date, display_name))

    return lst
