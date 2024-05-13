from datetime import (
    datetime, date,
    timedelta, timezone
)

utc_8 = timezone(timedelta(hours=8))

USER_UTC = utc_8

class StEventType:
    REGULAR = 'Regular'
    ALL_DAY = 'All day'
    FREE = 'Free'
    BOOKED = 'Not free'


class StEvent:
    def __init__(self, event_type: StEventType, t_start: date | datetime, t_end: date | datetime, summary: str,):
        self.event_type = event_type
        self.t_start = t_start if event_type == StEventType.ALL_DAY else self._ensure_datetime(t_start)
        self.t_end = t_end if event_type == StEventType.ALL_DAY else self._ensure_datetime(t_end)
        self.summary = str(summary)

        self.index = self._ensure_datetime(self.t_start)
        

    def __str__(self):
        t_start_str = self.t_start if self.event_type == StEventType.ALL_DAY else self.t_start.strftime('%Y-%m-%d %H:%M')
        t_end_str = self.t_end if self.event_type == StEventType.ALL_DAY else self.t_end.strftime('%Y-%m-%d %H:%M')

        return f"Event Type: {self.event_type}, Start: {t_start_str}, End: {t_end_str}, Summary: {self.summary}"


    def jsonify(self):
        if self.event_type == 'All day':
            return {
                'type': self.event_type,
                't_start': {
                    'year': self.t_start.year,
                    'month': self.t_start.month,
                    'date': self.t_start.day,
                },
                't_end': {
                    'year': self.t_end.year,
                    'month': self.t_end.month,
                    'date': self.t_end.day,
                },
                'summary': self.summary,
            }
        else:
            return {
                'type': self.event_type,
                't_start': self.t_start.timestamp(),
                't_end': self.t_end.timestamp(),
                'summary': self.summary,
            }
    
        
    @staticmethod
    def _ensure_datetime(dt):
        """Make sure the dt is in type of datetime without tzinfo (utc0)"""        
        if isinstance(dt, datetime):
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc)
            dt = dt.replace(tzinfo=None)
        elif isinstance(dt, date):
            dt = datetime(dt.year, dt.month, dt.day, tzinfo=USER_UTC).replace(tzinfo=None)
            
        return dt
    
    
if __name__ == '__main__':
    stEvent = StEvent(
        event_type=StEventType.REGULAR,
        t_start=datetime(2022, 1, 1, 8, 0, tzinfo=USER_UTC),
        t_end=datetime(2022, 1, 1, 9, 0, tzinfo=USER_UTC),
        summary='Regular Event Test'
    )
    
    print(stEvent)
    
    stEvent = StEvent(
        event_type=StEventType.ALL_DAY,
        t_start=date(2023, 1, 1),
        t_end=date(2023, 1, 2),
        summary='Regular Event Test'
    )
    
    print(stEvent)