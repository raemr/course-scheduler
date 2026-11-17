from dataclasses import dataclass, field


@dataclass
class block:
    start_time: int = 0
    end_time: int = 0
    days: list[str] = field(default_factory=list[str])
    locations: list[str] = field(default_factory=list[str])


@dataclass
class course:
    department: str = ""
    course_number: int = 0
    suffix: str = ""
    school: str = ""
    section: int = 0
    times: list[block] = field(default_factory=list[block])

    @property
    def key(self):
        return f"{self.department}{self.course_number}{self.suffix} {self.school}-{'0' + str(self.section) if self.section < 10 else self.section}"
