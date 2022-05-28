# mt-holidays

Generator of a file with non-working days for MikroTik routers.

## Usage
With system Python:
* Install Poetry: https://python-poetry.org/docs/#installation
* Type the following:
```shell
poetry install
poetry run mt-holidays --help
poetry run mt-holidays list-countries
poetry run mt-holidays generate RU holidays.txt
```

With Docker:
* Install Docker: https://docs.docker.com/desktop/
* Type the following:
```shell
docker build -t mt-holidays .
docker run --rm -v ${PWD}:/app mt-holidays --help
docker run --rm -v ${PWD}:/app mt-holidays list-countries
docker run --rm -v ${PWD}:/app mt-holidays generate RU holidays.txt
```

## Command line options
```shell
$ poetry run mt-holidays list-countries --help
Usage: mt-holidays list-countries [OPTIONS]

  Lists available countries or regions with their codes.

Options:
  --include-subregions / --no-include-subregions
                                  [default: no-include-subregions]
  --help                          Show this message and exit.

$ poetry run mt-holidays generate --help
Usage: mt-holidays generate [OPTIONS] ISO_CODE [FILE_OUTPUT]

  Generate file for any country using Workalendar.

Arguments:
  ISO_CODE       [required]
  [FILE_OUTPUT]  [default: -]

Options:
  --extra-working-days [%Y-%m-%d]
  --extra-holidays [%Y-%m-%d]
  --help                          Show this message and exit.

$ poetry run mt-holidays generate-ru --help
Usage: mt-holidays generate-ru [OPTIONS] CSVFILE [FILE_OUTPUT]

  Generate file for Russia using data.gov.ru export.

Arguments:
  CSVFILE        [required]
  [FILE_OUTPUT]  [default: -]

Options:
  --help  Show this message and exit.
```

## MikroTik script example
```
# get today's date
:local date [/system clock get date]
# read the file holidays.txt and cast it to the array
:local hdays [:toarray [/file get [/file find name=holidays.txt] contents]]
# check if $date in the array $hdays
:local isWork ([:typeof [:find $hdays $date -1]] = "nil")
:if ($isWork) do={
    # the code to run in working days
} else={
    # the code to run in non-working days
}
```
