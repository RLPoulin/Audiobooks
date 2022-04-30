## v0.8.0 (2022-04-30)

### Feat

- **app**: add flask app entry point

### Refactor

- **database**: remove redundent call to str

## v0.7.1 (2021-12-24)

### Refactor

- **db_tests**: change library_path to a module constant
- correct spelling and supress a few incorrect PyCharm warnings
- **models**: move ModelType from database to models

### Fix

- **log.LogManager**: improve logging level handling
- **log**: improve code for logging levels
- **models.Book**: clean class initializer, made genre optional
- **database.LibraryDatabase**: change filename property to a Path object file_path

## v0.7.0 (2021-12-24)

### Fix

- **database.CachedSession**: renamed CachedSession.get() to .get_instance() to remove conflict with parent method
- add traceback handling from Rich
- **log**: move more functionality to LogManager
- **log**: create a LogManager class to take care of logging functionality

### Refactor

- update code to new 3.10 syntax

### Feat

- **log**: migrate logging handler to Rich

## v0.6.0 (2021-12-20)

### Refactor

- update noqa comments for use with flake8
- **models**: fix type annotations after sqlalchemy-stubs update
- **audiobooks**: improve code with flakehell
- **myfunctions**: improve code with flakehell

### Fix

- **flakehell**: fix and clean config
- **models**: change clean_name() to use the titlecase library
- update typing information for Python 3.9 and mypy 0.800

### Feat

- update dependencies; includes increasing the Python version to 3.9

## v0.5.1 (2021-02-06)

### Refactor

- **audiobooks**: improve code with flakehell
- **myfunctions**: improve code with flakehell

### Fix

- **flakehell**: fix and clean config
- **models**: change clean_name() to use the titlecase library
- update typing information for Python 3.9 and mypy 0.800

## v0.5.0 (2021-02-06)

### Feat

- update dependencies; includes increasing the Python version to 3.9

### Refactor

- improves code to fix mypy errors

## v0.4.5 (2020-09-19)
