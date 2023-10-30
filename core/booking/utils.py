from datetime import datetime, timedelta

def Dateslotgenerator():
    # Get today's date
    input_date = datetime.now().date()
    lst = []

    # Define the number of weeks into the future and past
    weeks_in_future = 2
    weeks_in_past = 0

    # Define the names of the days of the week in the desired order
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    # Iterate through the days and add date and day name to the list
    for i in range(-7 * weeks_in_past, 7 * (weeks_in_future + 1)):
        date = input_date + timedelta(days=i)
        day_name = day_names[date.weekday()]
        formatted_date = date.strftime('%Y-%m-%d')
        day_week  = f"({day_name})"
        display_name = f"{formatted_date} | ({day_name})"
        lst.append((date,  display_name))

    return lst

#TODO


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
        time_slots.append(( f"{slot_start.strftime('%H:%M')}"))

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
        time_slots.append(( f" {slot_start.strftime('%H:%M')}"))

    return time_slots


