import argparse

def ranged_type(value_type, min_value=float("-inf"), max_value=float("inf")):
    """
    Validates that an argument is of a certain type and in range : min_value <= arg <= max_value

    Args:
        value_type: value-type to convert arg to
        min_value: Minimum acceptable value (included)
        max_value: Maximum acceptable value (included)

    Returns:
        function: Handle of an argument type function for ArgumentParser

    Examples:
        >>> ranged_type(float, 0.0, 1.0)
        >>> ranged_type(int, 10)
    """

    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f'must be a valid {value_type}')

        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f'must be within [{min_value}, {max_value}]')
        return f

    return range_checker
