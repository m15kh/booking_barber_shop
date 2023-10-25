

from datetime import datetime, timedelta

def generate_time_slots(start_time_str, finish_time_str, start_rest_str, finish_rest_str):
    slot_duration_minutes = 60
    # Convert start and finish times to datetime objects
    start_time = datetime.strptime(start_time_str, "%H:%M")
    finish_time = datetime.strptime(finish_time_str, "%H:%M")

    # Convert rest start and end times to datetime objects
    start_rest = datetime.strptime(start_rest_str, "%H:%M")
    finish_rest = datetime.strptime(finish_rest_str, "%H:%M")

    # Initialize a list to store the time slots
    time_slots = []

    # Initialize the current time as the start time
    current_time = start_time

    # Calculate the time difference between the current time and rest start time
    time_difference = start_rest - current_time

    # Calculate the number of slots before the rest period
    num_slots = int(time_difference.total_seconds() / (slot_duration_minutes * 60))

    # Generate time slots before the rest period
    for i in range(num_slots):
        slot_start = current_time + timedelta(minutes=i * slot_duration_minutes)
        slot_end = slot_start + timedelta(minutes=slot_duration_minutes)
        time_slots.append(( f"{slot_start.strftime('%H:%M')} – {slot_end.strftime('%H:%M')}"))

    # Set the current time to the end of the rest period
    current_time = finish_rest

    # Calculate the time difference between the last rest end time and the finish time
    time_difference = finish_time - current_time

    # Calculate the number of slots after the last rest period
    num_slots = int(time_difference.total_seconds() / (slot_duration_minutes * 60))

    # Generate time slots after the last rest period
    for i in range(num_slots):
        slot_start = current_time + timedelta(minutes=i * slot_duration_minutes)
        slot_end = slot_start + timedelta(minutes=slot_duration_minutes)
        time_slots.append(( f" {slot_start.strftime('%H:%M')} – {slot_end.strftime('%H:%M')}"))

    return time_slots

# Example usage:
start_time = "10:00"
finish_time = "17:00"
start_rest = "11:00"
finish_rest = "12:30"

timeslots = generate_time_slots(start_time, finish_time, start_rest, finish_rest)
for slot in timeslots:
    print(slot)


