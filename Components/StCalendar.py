from .StEvent import StEvent, StEventType

import icalendar
from enum import Enum, auto
from zoneinfo import ZoneInfo
from datetime import (
    datetime, date,
    timedelta, timezone
)

utc_8 = timezone(timedelta(hours=8))

USER_UTC = utc_8


# ---------------------------------- Division ----------------------------------

class StCalendar:
    def __init__(self, events=[]):
        self.events = events

    def __str__(self):
        if not self.events:
            return "No events in the calendar."
        events_str = '\n'.join(str(event) for event in self.events)
        return f"Calendar Events:\n{events_str}"
    
    
    def jsonify(self) -> list[dict]:
        return [e.jsonify() for e in self.events]
    
    
    def find_events_by_type(self, type: StEventType):
        events = [event for event in self.events if event.event_type == type]
        return StCalendar(events=events)
    
    
    def find_events_by_range(self, t_start: datetime, t_end: datetime):
        t_start, t_end = self._ensure_utc_datetime(t_start), self._ensure_utc_datetime(t_end)

        events = []
        for e in self.events:
            if e.utc_index[0] >= t_start:
                events.append(e)
                if e.utc_index[1] >= t_end:
                    break

        return StCalendar(events=events)


    @staticmethod
    def _ensure_utc_datetime(dt: datetime) -> datetime:
        if isinstance(dt, datetime):
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc)
            dt = dt.replace(tzinfo=None)
            
        return dt


class StGoogleCalendar(StCalendar):
    def __init__(self, ics_file_path=r'./data/test/basic.ics'):
        
        with open(ics_file_path, 'r', encoding='utf-8') as f:
            calendar = icalendar.Calendar.from_ical(f.read())
        
        super().__init__(events=self.get_events_from_calendar(calendar))
        
        
    @staticmethod
    def get_events_from_calendar(calendar):
        """"""
        events = []

        for event in calendar.walk('VEVENT'):
            dtstart = event.get('dtstart').dt
            dtend = event.get('dtend').dt

            if isinstance(dtstart, date) and isinstance(dtend, date) and not (isinstance(dtstart, datetime)) and not (isinstance(dtend, datetime)):
                # All day Event

                events.append(
                    StEvent(StEventType.ALL_DAY, dtstart, dtend, event.get('summary'))
                )

            elif isinstance(dtstart, datetime) and isinstance(dtend, datetime):
                # Regular Event
                
                events.append(
                    StEvent(StEventType.REGULAR, dtstart, dtend, event.get('summary'))
                )

        events = sorted(events, key=lambda event: event.utc_index[0])
        
        return events
        


if __name__ == '__main__':
    stCalendar = StGoogleCalendar()
    print(stCalendar)