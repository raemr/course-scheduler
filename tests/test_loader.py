from course_scheduler.structs import block, course


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
