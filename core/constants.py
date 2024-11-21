from enum import StrEnum


class APP(StrEnum):
    SCHEDULE = 'schedule'
    CLIENT = 'clients'


class ROUTER(StrEnum):
    CLIENT = 'client'
    LESSON = 'lesson'
    GROUP = 'group'
    TEACHER = 'teacher'
    SUBJECT = 'subject'
    ROOM = 'room'
    FACULTY = 'faculty'
    TIMESLOT = 'timeslot'
