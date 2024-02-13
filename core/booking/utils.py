from datetime import datetime, timedelta


def Dateslotgenerator(exclude_namedays=None, exclude_dates=None):
    # Get today's date
    input_date = datetime.now().date()
    lst = []

    # Define the number of weeks into the future and past
    weeks_in_future = 2

    # Define the names of the days of the week in the desired order
    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Convert the exclude_days to lowercase for case-insensitive comparison
    exclude_days_lower = (
        [day.lower() for day in exclude_namedays] if exclude_namedays else []
    )

    # Convert the exclude_dates to a set of strings for efficient comparison
    exclude_dates_set = set(exclude_dates) if exclude_dates else set()

    # Iterate through the days and add date and day name to the list
    for i in range(7 * (weeks_in_future + 1)):
        date = input_date + timedelta(days=i)
        day_name = day_names[date.weekday()]

        # Check if the current day is in the list of excluded days or matches any excluded date, and skip it if needed
        if (exclude_days_lower and day_name.lower() in exclude_days_lower) or (
            exclude_dates_set and date.strftime("%Y-%m-%d") in exclude_dates_set
        ):
            continue

        formatted_date = date.strftime("%Y-%m-%d")
        display_name = f"{formatted_date} | ({day_name})"
        lst.append((date, display_name))

    return lst



def TimeSlotgenerator(workstart, workfinish, reststart, restfinish, duration):
    # Convert start and finish times to datetime objects
    workstart = datetime.strptime(workstart, "%H:%M")
    workfinish = datetime.strptime(workfinish, "%H:%M")

    # Convert rest start and end times to datetime objects
    reststart = datetime.strptime(reststart, "%H:%M")
    restfinish = datetime.strptime(restfinish, "%H:%M")

    # Initialize a list to store the time slots
    time_slots = []

    # Initialize the current time as the start time
    current_time = workstart

    # Calculate the time difference between the current time and rest start time
    time_difference = reststart - current_time

    # Calculate the number of slots before the rest period
    num_slots = int(time_difference.total_seconds() / (duration * 60))

    # Generate time slots before the rest period
    for i in range(num_slots):
        slot_start = current_time + timedelta(minutes=i * duration)
        slot_end = slot_start + timedelta(minutes=duration)
        time_slots.append((f"{slot_start.strftime('%H:%M')}"))

    # Set the current time to the end of the rest period
    current_time = restfinish

    # Calculate the time difference between the last rest end time and the finish time
    time_difference = workfinish - current_time

    # Calculate the number of slots after the last rest period
    num_slots = int(time_difference.total_seconds() / (duration * 60))

    # Generate time slots after the last rest period
    for i in range(num_slots):
        slot_start = current_time + timedelta(minutes=i * duration)
        slot_end = slot_start + timedelta(minutes=duration)
        time_slots.append((f"{slot_start.strftime('%H:%M')}"))

    len_time_slots = len(time_slots)
    return time_slots, len_time_slots
