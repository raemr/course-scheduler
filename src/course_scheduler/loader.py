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


# def test_course_schema(courses: dict) -> None:
#
#     count = 0
#
#     for course in courses:
#         if count < 3:
#             print(json.dumps(course, indent=4), "\n\n\n")
#             count += 1
#         else:
#             raise SystemExit("run 3 times")
#


def validate_course_keys(courses: list[dict]) -> bool:
    """
    Checks whether courses is in fact a list of dicts, and then validates whether the keys in that dict are consistent across each course entry.

    Args:
        courses: list of dicts (hopefully?).

    Returns:
        A boolean of whether courses is in fact a list of dicts, and whether they all have the same schema.
    """
    for i in range(len(courses)):
        if type(courses[i]).__name__ != "dict":
            return False

    first_course_keys = courses[0].keys()

    for i in range(1, len(courses)):
        if courses[i].keys() != first_course_keys:
            return False

    return True


def dict_list_to_course_list(dict_list: list[dict]) -> list[course]:

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


def search_raw_course(deptartment: str, number: int, courses: list[dict]) -> list[dict]:
    course_list = [
        course
        for course in courses
        if (
            course["identifier"]["department"] == deptartment
            and course["identifier"]["courseNumber"] == number
        )
    ]

    return course_list


def search_course_basic(
    department: str, number: int, courses: list[course]
) -> list[course]:
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

    # for key in course:
    #     print(f"KEY {key}: {course[key]} \n")

    for key, item in course.items():
        print(f"KEY {key}: {item} \n")


if __name__ == "__main__":
    courses_raw = file_loader("./src/data/SP2027.json")

    courses_list = dict_list_to_course_list(courses_raw)

    # results = search_course_basic("MATH", 127, courses_list)

    results = match_search_course(
        courses=courses_list, department="CSCI", school="PO", suffix="AG"
    )

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

    if not results:
        print(*[f"COURSE {course_}" for course_ in results], sep="\n")
    # out = search_course(dept="MATH", number=127, courses=courses)

    #
    # if out:
    #     print_course(out[0])
