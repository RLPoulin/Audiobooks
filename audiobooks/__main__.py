"""Program entry point. Currently, it just runs the db tests."""

from audiobooks.db_tests import do_tests


def main() -> None:
    """Execute the entry point of the program."""
    do_tests()


if __name__ == "__main__":
    main()
