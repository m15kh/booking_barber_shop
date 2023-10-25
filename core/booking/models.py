from django.db import models
from django.contrib.auth import get_user_model

# local
from .utilities import order_date
from .time_manager import generate_time_slots


CustomUser = get_user_model()



class Appointment_Hour(models.Model):
    # DAYS_OF_WEEK = (
    #     (0, "Saturday"),
    #     (1, "Sunday"),
    #     (2, "Monday"),
    #     (3, "Tuesday"),
    #     (4, "Wednesday"),
    #     (5, "Thursday"),
    #     (6, "Friday"),
    # )

    # Days = models.IntegerField(
    #     choices=DAYS_OF_WEEK, unique=True
    # )  # Add unique constraint here

    start_hour = models.TimeField()
    end_hour = models.TimeField()
    start_rest_hour = models.TimeField()
    duration = models.IntegerField(choices=((15, "15 minute"), (30, "30 minute"), (45, "45 minute"), (60, "60 minute")))
    finish_rest_hour = models.TimeField()

    def __str__(self):
        # day_name = self.get_Days_display()
        return " {} {} {} {}".format(
            # day_name,
            self.start_hour,
            self.end_hour,
            self.start_rest_hour,
            self.finish_rest_hour,
        )





class Appointment(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = (
            "barber",
            "date",
            "timeslot",
        )  # you can't have multiple appointments with the same barber on the same date and timeslot.

    TIMESLOT_LIST = (
        (0, "09:00 – 09:30"),
        (1, "10:00 – 10:30"),
        (2, "11:00 – 11:30"),

    )

    barber = models.ForeignKey("Barber", on_delete=models.CASCADE)
    date = models.DateTimeField(choices=order_date())


    appointment_hours = Appointment_Hour.objects.all()
    timeslot = models.DateField(
        appointment_hours
            )
    print(appointment_hours)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    

    def __str__(self):
        return "{} {} {}. customer: {}".format(
            self.date, self.time, self.barber, self.customer
        )

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Barber(models.Model):
    """Stores info about barber"""

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.last_name, self.short_name)

    @property
    def short_name(self):
        return "{} {}.{}.".format(
            self.last_name.title(),
            self.first_name[0].upper(),
            self.middle_name[0].upper(),
        )


class Appointment_Hour(models.Model):
    # DAYS_OF_WEEK = (
    #     (0, "Saturday"),
    #     (1, "Sunday"),
    #     (2, "Monday"),
    #     (3, "Tuesday"),
    #     (4, "Wednesday"),
    #     (5, "Thursday"),
    #     (6, "Friday"),
    # )

    # Days = models.IntegerField(
    #     choices=DAYS_OF_WEEK, unique=True
    # )  # Add unique constraint here

    start_hour = models.TimeField()
    end_hour = models.TimeField()
    start_rest_hour = models.TimeField()
    duration = models.IntegerField(choices=((15, "15 minute"), (30, "30 minute"), (45, "45 minute"), (60, "60 minute")))
    finish_rest_hour = models.TimeField()

    def __str__(self):
        # day_name = self.get_Days_display()
        return " {} {} {} {}".format(
            # day_name,
            self.start_hour,
            self.end_hour,
            self.start_rest_hour,
            self.finish_rest_hour,
        )


