from StEvent import StEvent, StEventType

import icalendar
from enum import Enum, auto
from zoneinfo import ZoneInfo
from datetime import (
    datetime, date,
    timedelta, timezone
)

utc_8 = timezone(timedelta(hours=8))

USER_UTC = utc_8

def get_events_from_calendar(calendar):
    """"""
    events = []

    for event in calendar.walk('VEVENT'):
        dtstart = event.get('dtstart').dt
        dtend = event.get('dtend').dt

        if isinstance(dtstart, date) and isinstance(dtend, date) and not (isinstance(dtstart, datetime)) and not (isinstance(dtend, datetime)):
            # 全天事件
            # print('')
            # print(dtstart, dtend, event.get('summary'))
            events.append(
                StEvent(StEventType.ALL_DAY, dtstart, dtend, event.get('summary'))
            )

        elif isinstance(dtstart, datetime) and isinstance(dtend, datetime):
            # 常规事件
            # print('')
            # print(dtstart.astimezone(utc_8), dtend.astimezone(utc_8), event.get('summary'))
            events.append(
                StEvent(StEventType.REGULAR, dtstart, dtend, event.get('summary'))
            )

    events = sorted(events, key=lambda event: event.index)
    
    return events


def find_events_in_range(t_start: datetime, t_end: datetime):
    pass


class StCalendar:
    def __init__(self, events=[]):
        self.events = events
        self.free_events = []

    def __str__(self):
        if not self.events:
            return "No events in the calendar."
        events_str = '\n'.join(str(event) for event in self.events)
        return f"Calendar Events:\n{events_str}"

    def find_events_by_type(self, type: StEventType):
        return StCalendar(events=[event for event in self.events if event.event_type == type])
        

    def jsonify(self):
        json_data = []
        for e in self.events:
            json_data.append(e.jsonify())
        return json_data
    

if __name__ == '__main__':
    ics_file_path = r'./data/test/basic.ics'

    with open(ics_file_path, 'r', encoding='utf-8') as f:
        calendar = icalendar.Calendar.from_ical(f.read())
        events = get_events_from_calendar(calendar)
    
    stCalendar = StCalendar(events=events)
    print(stCalendar.jsonify())