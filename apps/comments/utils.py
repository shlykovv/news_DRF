from rest_framework.serializers import ValidationError
from check_swear import SwearingCheck


def validate_comment_check(value: str) -> str | ValidationError:
    """Function to check for bad words inside a comment

    Args:
        value (str): Values ​​to check(Comment)

    Raises:
        ValidationError: Error if comment does not pass verification

    Returns:
        str: Return a validated comment or an error of type ValidationError
    """    
    sch = SwearingCheck()
    if sch.predict(value)[0] == 1:
        raise ValidationError("The comment contains obscene language.")
    return value
