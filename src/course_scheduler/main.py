"""
# TODO:
Make the parser
Make the check valid
Make the make permutations
"""

from dataclasses import dataclass
from datetime import time


@dataclass
class course:
    department: str
    code: int
    school: str
    time: list[list[time]]
    days: list[str]


@dataclass
class schedule:
    courses: list[course]


def generate_schedule_combinations(courses: list[course]) -> list[schedule]:
    del courses
    raise NotImplementedError("bruh calm")


def verify_schedule(schedule: schedule) -> bool:
    del schedule
    raise NotImplementedError("yo chill")


sample_course_math129 = course(
    "MATH",
    129,
    "HM",
    [[time(13, 15), time(14, 30)], [time(13, 15), time(14, 30)]],
    ["m", "w"],
)

sample_schedule = schedule([sample_course_math129])


if __name__ == "__main__":
    print(verify_schedule(sample_schedule))
