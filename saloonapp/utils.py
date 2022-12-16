import datetime
from typing import Union, Optional, Any

from django.conf import settings

from .models import Saloon
from .models import Note


def construct_free_day_schedule() -> list[datetime.time]:
    minutes_in_hour = 60
    workday_start = settings.WORKDAY_START
    workday_end = settings.WORKDAY_END
    note_interval_in_minutes = settings.NOTE_INTERVAL_IN_MINUTES

    timeslot = workday_start
    timeslots = [timeslot]
    i = 0
    while timeslot <= workday_end:
        minutes = timeslot.hour * minutes_in_hour + timeslot.minute + note_interval_in_minutes
        hours = minutes // minutes_in_hour
        minutes %= minutes_in_hour
        timeslot = datetime.time(hour=hours, minute=minutes)
        timeslots.append(timeslot)
        i += 1

    return timeslots


def construct_free_calendar_with_filters(
        weekday: Union[str, int], filters: dict[str, Any]) -> list[dict[str, Any]]:
    """Construct free calendar for day with saloon filters."""
    filters['masterlinks__weekdays__isoweekday'] = weekday
    saloons = Saloon.objects. \
        prefetch_related(
        'masterlinks',
        'masterlinks__master',
        'masterlinks__master__services',
        'masterlinks__master__speciality'
    ). \
        exclude(masterlinks__isnull=True). \
        filter(**filters).distinct()
    calendar = []
    free_day = construct_free_day_schedule()
    for saloon in saloons:
        calendar_saloon = {'saloon': saloon.to_dict(), 'masters_schedule': []}
        for masterlink in saloon.masterlinks.all():
            # if service_pk and not masterlink.master.services.filter(pk=service_pk):
            #     continue
            calendar_saloon['masters_schedule'].append(
                {
                    'master': masterlink.master.to_dict(),
                    'timeslots': free_day
                }
            )
        if calendar_saloon['masters_schedule']:
            calendar.append(calendar_saloon)
    return calendar


def construct_calendar_by_filters(
        date: datetime.date,
        saloon_pk: Optional[int] = None,
        master_pk: Optional[int] = None,
        service_pk: Optional[int] = None
):
    """Construct calendar for day with filters by saloon, master, service."""
    filters = {'date': date}
    calendar_filters = {}  # filters for construct_free_calendar_with_filters
    if saloon_pk:
        filters['saloon__pk'] = saloon_pk
        calendar_filters['pk'] = saloon_pk

    if master_pk:
        filters['master__pk'] = master_pk
        calendar_filters['masterlinks__master__pk'] = master_pk

    if service_pk:
        # no need filter notes by service, because this filter for free time, not for busy
        calendar_filters['masterlinks__master__services'] = service_pk

    calendar = construct_free_calendar_with_filters(date.isoweekday(), calendar_filters)

    notes = Note.objects.select_related('saloon', 'master', 'master__speciality', 'service').filter(**filters)

    for note in notes:
        saloon_index = None
        for saloon_timeslots_index, saloon_timeslots in enumerate(calendar):
            if saloon_timeslots['saloon']['pk'] == note.saloon.pk:
                saloon_index = saloon_timeslots_index
                break
        if saloon_index is None:
            continue

        master_index = None
        for master_timeslots_index, master_timeslots in enumerate(saloon_timeslots['masters_schedule']):
            if master_timeslots['master']['pk'] == note.master.pk:
                master_index = master_timeslots_index
                break
        if master_index is None:
            continue

        master_timeslots_copy = master_timeslots['timeslots'].copy()
        for timeslot_index, timeslot in enumerate(master_timeslots['timeslots']):
            if note.stime <= timeslot < note.etime:
                master_timeslots_copy.remove(timeslot)
        calendar[saloon_index]['masters_schedule'][master_index]['timeslots'] = master_timeslots_copy
    return calendar
