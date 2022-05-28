# mt-holidays

Generator of a file with non-working days for MikroTik routers.

## Usage
With system Python:
```shell
poetry install
poetry run mt-holidays --help
poetry run mt-holidays list-countries
poetry run mt-holidays generate RU holidays.txt
```

With Docker:
```shell
docker build -t mt-holidays .
docker run --rm -v ${PWD}:/app mt-holidays --help
docker run --rm -v ${PWD}:/app mt-holidays list-countries
docker run --rm -v ${PWD}:/app mt-holidays generate RU holidays.txt
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
