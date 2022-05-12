## v0.9.0 (2022-05-01)

### Refactor

- **database**: remove the entire database module since flask-sqlalchemy takes care of everything now
- **library**: move models to new audiobooks.library package and update code to use flask-sqlalchemy
- **log**: remove audiobooks.log module

### Feat

- ****main****: change main() to create the Flask app and run it; add logging setup
- **app**: change from a simple app to a create_app() factory and integrate new extensions and pages
- **library**: add simple pages to create and read entries from the database
- **configuration**: add module to prepare the default configuration for Flask
- **extensions**: add module to initialize Flask plugins
- **main_page**: add module for the application main page with a basic landing page

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
