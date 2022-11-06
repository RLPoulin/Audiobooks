## v0.11.2 (2022-11-06)

### Fix

- **app**: fix for Flask-SQLAlchemy v3.0 API

## v0.11.1 (2022-06-04)

### Fix

- **database**: fix _simplify_description for compatibility with python 3.9

### Refactor

- **database.Model**: improve the implementation of the to_dict method
- **library.models**: replace the LIBRARY_MODELS dict with an enum and get_library_item function

## v0.11.0 (2022-05-29)

### Fix

- **audiobooks.configuration**: fix base config to not crash during testing without a .env file
- **audiobooks.library.routes**: fix annotations
- **audiobooks.library.routes**: improve error handling
- **audiobooks.database**: add KeyError exception to Model.update to prevent creating non-existant attributes
- **library.utils**: fix bug in clean_name due to inconsistent casing
- **database**: fix handling of None values in Model.get_by_id and Model.get
- **database.SqliteDecimal**: set cache_ok property to True
- **library.models**: fix Decimal implementation for compatibility with sqlite
- fix a few small bugs

### Refactor

- **audiobooks.configuration**: move configuration to Config class
- **configuration**: move LOG_LEVEL from __main__ to configuration
- add compatibility with python 3.9

## v0.10.0 (2022-05-14)

### Feat

- **library.routes**: update routes to use the new CRUD methods from database.Model and library.models.LibraryModel
- **library.models**: update models to the new audiobooks.database.Model base class
- **database.Model**: add to_dict() method
- **database**: add new database base model class

### Fix

- **routes**: improve route responses
- **database.Model**: improve to_dict method
- ****main****: fix script entry point

## v0.9.0 (2022-05-01)

### Feat

- **main**: change main() to create the Flask app and run it; add logging setup
- **app**: change from a simple app to a create_app() factory and integrate new extensions and pages
- **library**: add simple pages to create and read entries from the database
- **configuration**: add module to prepare the default configuration for Flask
- **extensions**: add module to initialize Flask plugins
- **main_page**: add module for the application main page with a basic landing page

## v0.8.0 (2022-04-30)

### Feat

- **app**: add flask app entry point

## v0.7.1 (2021-12-24)

### Fix

- **log.LogManager**: improve logging level handling
- **log**: improve code for logging levels
- **models.Book**: clean class initializer, made genre optional
- **database.LibraryDatabase**: change filename property to a Path object file_path

## v0.7.0 (2021-12-24)

### Feat

- **log**: migrate logging handler to Rich

### Fix

- **database.CachedSession**: renamed CachedSession.get() to .get_instance() to remove conflict with parent method
- add traceback handling from Rich
- **log**: move more functionality to LogManager
- **log**: create a LogManager class to take care of logging functionality

## v0.6.0 (2021-12-20)

### Feat

- update dependencies; includes increasing the Python version to 3.9

### Fix

- **flakehell**: fix and clean config
- **models**: change clean_name() to use the titlecase library
- update typing information for Python 3.9 and mypy 0.800

## v0.5.1 (2021-02-06)

### Fix

- **flakehell**: fix and clean config
- **models**: change clean_name() to use the titlecase library
- update typing information for Python 3.9 and mypy 0.800

## v0.5.0 (2021-02-06)

### Feat

- update dependencies; includes increasing the Python version to 3.9
