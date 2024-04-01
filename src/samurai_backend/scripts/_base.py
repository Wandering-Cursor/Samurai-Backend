from typing import Literal


def colored_print(
    text: str,
    level: Literal["notset", "info", "warning", "error", "unexpected", "success"] = "notset",
) -> None:
    colors = {
        "error": "\033[91m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "info": "\033[94m",
        "unexpected": "\033[95m",
        "notset": "\033[97m",
    }
    reset = "\033[0m"

    if level not in colors:
        raise ValueError(f"Invalid color. Choose one of: {colors.keys()}")

    print(f"{colors[level]}{level.upper()}{reset}: {colors[level]}{text}{reset}")  # noqa: T201


if __name__ == "__main__":
    colored_print("Demo, to see how different colors look:\n", "warning")

    colored_print("This is a success message", "success")
    colored_print("This is an unexpected message", "unexpected")
    colored_print("This is an error message", "error")
    colored_print("This is a warning message", "warning")
    colored_print("This is an info message", "info")
    colored_print("This is a notset message", "notset")
