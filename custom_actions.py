import argparse
from utils import parse_date


class DeadlineAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # keywords for erasing deadline
        no_deadline_keywords = {"unset", "no", "false"}

        deadline_value = ""

        if len(values) > 2:
            raise argparse.ArgumentError(self, "deadline must contain maximum 2 values")
        elif len(values) == 1 and values[0].lower() in no_deadline_keywords:
            deadline_value = "no"
        else:
            date_str = " ".join(values)
            deadline_value = parse_date(date_str)

        setattr(namespace, self.dest, deadline_value)


class MultipleStatusAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        unique_values = set(values)
        unique_values.discard(self.default)

        status_value = "all" if len(unique_values) == 0 else unique_values

        setattr(namespace, self.dest, status_value)
