from dataclasses import dataclass


@dataclass
class course:
    department: str
    course_number: int
    suffix: str
    school: str
    section: int
    times: list[block]


@dataclass
class block:
    start_time: int
    end_time: int
    days: list[str]
    locations: list[str]
