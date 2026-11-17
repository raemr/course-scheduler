import json

from .structs import block, course


def file_loader(course_file_path: str) -> list[dict]:
    """
    Loads the contents of a file into a variable.

    Args:
        course_file_path: string file path of json to load.

    Returns:
        list of courses, which are hopefully dicts.
    """
    with open(course_file_path, "r", encoding="utf-8") as courses_file:
        courses = json.load(courses_file)
        return courses


def dict_list_to_course_list(dict_list: list[dict]) -> list[course]:
    """
    Takes a loaded file's list[dict] representation and returns a list[course] representation.

    Args:
        dict_list: List of dicts from the json.load()

    Returns:
        A list of course objects for the given input.
    """

    def dict_to_course(course_dict: dict):

        def times_to_blocks(blocks: list[dict]) -> list[block]:
            return [
                block(
                    start_time=time["startTime"],
                    end_time=time["endTime"],
                    days=time["days"],
                    locations=time["locations"],
                )
                for time in blocks
            ]

        return course(
            department=course_dict["identifier"]["department"],
            course_number=course_dict["identifier"]["courseNumber"],
            suffix=course_dict["identifier"]["suffix"],
            school=course_dict["identifier"]["affiliation"],
            section=course_dict["identifier"]["sectionNumber"],
            times=times_to_blocks(course_dict["schedules"]),
        )

    return [dict_to_course(course_dict) for course_dict in dict_list]


def search_raw_courses(department: str, number: int, courses: list[dict]) -> list[dict]:
    """
    Search functionality for a raw list[dict] course list.

    Args:
        department: The desired department code.
        number: The desired course course number.
        courses: The raw list[dict] to search through.

    Returns:
        A list of courses that match the requirements, [] if none do.
    """
    course_list = [
        course
        for course in courses
        if (
            course["identifier"]["department"] == department
            and course["identifier"]["courseNumber"] == number
        )
    ]

    return course_list


def search_course_basic(
    department: str, number: int, courses: list[course]
) -> list[course]:
    """
    Basic search functionality for a list[course] course list.

    Args:
        department: The desired department code.
        number: The desired course number.
        courses: The list[course] to search through.

    Returns:
        A list of course objects that match the requirements, [] if none do.
    """
    course_list = [
        course
        for course in courses
        if (course.department == department and course.course_number == number)
    ]

    return course_list


def match_search_course(
    courses: list[course],
    department: str | None = None,
    course_number: int | None = None,
    suffix: str | None = None,
    school: str | None = None,
    section: int | None = None,
) -> list[course]:

    return [
        course_
        for course_ in courses
        if (
            department in [course_.department, None]
            and course_number in [course_.course_number, None]
            and suffix in [course_.suffix, None]
            and school in [course_.school, None]
            and section in [course_.section, None]
        )
    ]


def better_course_search(courses: list[course], **filters) -> list[course]:
    """Each filter will take a lambda, for each key in filter, do filter[key](getattr(c, key))"""
    return [
        course_
        for course_ in courses
        if all(
            (
                condition(getattr(course_, field))
                if callable(condition)
                else getattr(course_, field) == condition
            )
            for field, condition in filters.items()
        )
    ]


def print_raw_course(course: dict) -> None:
    for key, item in course.items():
        print(f"KEY {key}: {item} \n")


if __name__ == "__main__":
    courses_raw = file_loader("./src/data/SP2027.json")

    courses_list = dict_list_to_course_list(courses_raw)

    print(
        *better_course_search(
            courses=courses_list,
            department="MATH",
            course_number=lambda i: bool(0 <= i <= 100),
            school="HM",
            times=lambda blocks: all(
                bool(block_.start_time > 14 * 3600 + 45 * 60)
                for block_ in blocks
                if "M" in block_.days
            ),
        ),
        sep="\n",
    )
