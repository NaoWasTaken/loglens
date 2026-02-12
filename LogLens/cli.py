import click
import re
from datetime import datetime

@click.command()
@click.argument('file')
@click.option('--findcodes', is_flag=True)
@click.option('--informationalonly', is_flag=True)
@click.option('--successonly', is_flag=True)
@click.option('--redirectonly', is_flag=True)
@click.option('--errorsonly', is_flag=True)
@click.option('--apache', is_flag=True)
@click.option('--json', is_flag=True)
@click.option('--nginx', is_flag=True)
@click.option('--from-date', type=str, help='Start date: mm/dd/yyyy')
@click.option('--to-date', type=str, help='End date: mm/dd/yyyy')
def analyze(file, findcodes, informationalonly, successonly, redirectonly, errorsonly, apache, json, nginx, from_date, to_date):

    format_flags = [apache, json, nginx]
    code_flags = [findcodes, informationalonly, successonly, redirectonly, errorsonly]

    if sum(format_flags) > 1 or sum(code_flags) > 1:
        print("Only one format or search flag accepted")
        return

    format_map = {
        "apache": ("apache", 8),
        "json": ("json", 5),
        "nginx": ("nginx", 8),
    }

    if apache:
        log_format, index = format_map["apache"]

    elif json:
        log_format, index = format_map["json"]

    elif nginx:
        log_format, index = format_map["nginx"]

    else:
        print("Please specify a log format: --apache, --json, or --nginx")
        return

    try:
        lines = read(file)
        from_date, to_date = date_filter(from_date, to_date)
        type, code_xx = process(lines, index, findcodes, informationalonly, successonly, redirectonly, errorsonly, from_date, to_date, log_format)

        if not findcodes:
            if informationalonly or successonly or redirectonly or errorsonly:
                statement = codes_print(type, code_xx)
                print(statement)

    except FileNotFoundError:
        print(f"Error: Could not find file '{file}'")

    except PermissionError:
        print(f"Error: No permission to read '{file}'")

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occured: {e}")

def read(file):

    with open(file) as fd:
        return fd.readlines()

def codes_print(type, code):

    statement = f"{type} Codes Found - {code}"

    return statement

def parse_line_date(line, log_format):

    try:
        if log_format in ("apache", "nginx"):
            match = re.search(r'\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})\s[+-]\d{4}\]', line)
            if match:
                return datetime.strptime(match.group(1), "%d/%b/%Y:%H:%M:%S")

        elif log_format == "json":
            match = re.search(r'"time"\s*:\s*"([^"]+)"', line)
            if match:
                return datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")

    except ValueError:
        pass

    return None

def in_date_range(line_date, from_date, to_date):

    if line_date is None:
        return True

    if from_date and line_date < from_date:
        return False

    if to_date and line_date > to_date:
        return False

    return True

def count(lines, index, from_date, to_date, log_format):

    code_1xx = 0
    code_2xx = 0
    code_3xx = 0
    code_4xx = 0
    code_5xx = 0

    for _ in lines:
        if from_date or to_date:
            line_date = parse_line_date(_, log_format)
            if not in_date_range(line_date, from_date, to_date):
                continue

        codes = _.split()
        try:
            if codes[index][0] == "1":
                code_1xx += 1

            elif codes[index][0] == "2":
                code_2xx += 1

            elif codes[index][0] == "3":
                code_3xx += 1

            elif codes[index][0] == "4":
                code_4xx += 1

            elif codes[index][0] == "5":
                code_5xx += 1

        except IndexError:
            continue

    return code_1xx, code_2xx, code_3xx, code_4xx, code_5xx

def get_type(informationalonly, successonly, redirectonly, errorsonly, code_1xx, code_2xx, code_3xx, code_4xx, code_5xx):

    if informationalonly:
        return "Informational", code_1xx

    if successonly:
        return "Success", code_2xx

    if redirectonly:
        return "Redirectional", code_3xx

    if errorsonly:
        return "Error", code_4xx + code_5xx

    return None, 0

def process(lines, index, findcodes, informationalonly, successonly, redirectonly, errorsonly, from_date, to_date, log_format):

    if findcodes or errorsonly or informationalonly or successonly or redirectonly:
        code_1xx, code_2xx, code_3xx, code_4xx, code_5xx = count(lines, index, from_date, to_date, log_format)

        if findcodes:
            print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

        return get_type(informationalonly, successonly, redirectonly, errorsonly, code_1xx, code_2xx, code_3xx, code_4xx, code_5xx)

    return None, 0

def date_filter(fromdate, todate):

    try:
        if fromdate and todate:
            return datetime.strptime(fromdate, "%m/%d/%Y"), datetime.strptime(todate, "%m/%d/%Y")

        elif fromdate:
            return datetime.strptime(fromdate, "%m/%d/%Y"), None

        elif todate:
            return None, datetime.strptime(todate, "%m/%d/%Y")

    except ValueError:
        raise ValueError(f"Invalid date format. Expected mm/dd/yyyy, e.g. 01/31/2025")

    return None, None


if __name__ == "__main__":
    analyze()