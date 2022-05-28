import csv
from datetime import date, timedelta, datetime
from typing import Optional, Type, List

import typer
from workalendar.core import Calendar
from workalendar.registry import registry


app = typer.Typer()


@app.command()
def list_countries(include_subregions: bool = False) -> None:
    """
    Lists available countries or regions with their codes.
    """
    calendars = registry.get_calendars(include_subregions=include_subregions)
    for code, calendar_class in sorted(calendars.items()):
        typer.echo(f'{code}: {calendar_class.name}')


@app.command()
def generate(
    iso_code: str, file_output: typer.FileTextWrite = typer.Argument('-'),
    extra_working_days: List[datetime] = typer.Option(None, formats=['%Y-%m-%d']),
    extra_holidays: List[datetime] = typer.Option(None, formats=['%Y-%m-%d']),
) -> None:
    """
    Generate file for any country using Workalendar.
    """
    calendar_class: Optional[Type[Calendar]] = registry.get(iso_code)
    if not calendar_class:
        typer.echo(f'Calendar for "{iso_code}" ISO code not found', err=True)
        raise typer.Abort
    calendar: Calendar = calendar_class()

    current_date = date.today()
    non_working_days: List[str] = []
    while len(non_working_days) < 4096 // 12:
        while calendar.is_working_day(current_date, extra_working_days, extra_holidays):
            current_date += timedelta(days=1)
        non_working_days.append(current_date.strftime('%b/%d/%Y').lower())
        current_date += timedelta(days=1)
    file_output.write(','.join(non_working_days))
    typer.echo(
        'File generated',
        err=file_output.name == '<stdout>'
    )


@app.command()
def generate_ru(csvfile: typer.FileText, file_output: typer.FileTextWrite = typer.Argument('-')) -> None:
    """
    Generate file for Russia using data.gov.ru export.
    """
    today = date.today()
    non_working_days: List[str] = []

    reader = csv.reader(csvfile)
    for row in reader:
        try:
            year = int(row[0])
        except ValueError:
            continue
        if today.year > year:
            continue
        for month in range(1, 13):
            days = row[month].split(',')
            for day in days:
                try:
                    nwd = date(year, month, int(day))
                except ValueError:
                    continue
                if today > nwd:
                    continue
                non_working_days.append(nwd.strftime('%b/%d/%Y').lower())
                if len(non_working_days) >= 4096 // 12:
                    file_output.write(','.join(non_working_days))
                    typer.echo(
                        'File generated',
                        err=file_output.name == '<stdout>'
                    )
                    return


if __name__ == "__main__":
    app()
