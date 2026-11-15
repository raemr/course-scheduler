import json


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


def test_course_schema(courses: dict) -> None:

    count = 0

    for course in courses:
        if count < 3:
            print(json.dumps(course, indent=4), "\n\n\n")
            count += 1
        else:
            raise SystemExit("run 3 times")


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


if __name__ == "__main__":
    courses = file_loader("./src/data/SP2027.json")

    print(validate_course_keys(courses))
