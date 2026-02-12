import click
import re
from datetime import datetime

# TODO: maybe add more codes later
CODE_EXPLANATIONS = {
    "100": "Continue - server got the headers, client can keep going",
    "101": "Switching Protocols - server is switching to a different protocol as requested",
    "200": "OK - request worked",
    "201": "Created - request worked and a new resource was created",
    "204": "No Content - request worked but nothing to return",
    "301": "Moved Permanently - resource has a new permanent URL",
    "302": "Found - resource temporarily lives somewhere else",
    "304": "Not Modified - cached version is still good, no need to re-send",
    "400": "Bad Request - server couldn't parse or understand the request",
    "401": "Unauthorized - need to authenticate first",
    "403": "Forbidden - server understood but won't allow it",
    "404": "Not Found - resource doesn't exist at this URL",
    "405": "Method Not Allowed - that HTTP method isn't supported here",
    "408": "Request Timeout - server gave up waiting for the client",
    "429": "Too Many Requests - slow down, rate limit hit",
    "500": "Internal Server Error - something broke on the server side",
    "501": "Not Implemented - server doesn't support whatever was requested",
    "502": "Bad Gateway - got a bad response from an upstream server",
    "503": "Service Unavailable - server can't handle requests right now",
    "504": "Gateway Timeout - upstream server didn't respond in time",
}

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
@click.option('--explain', is_flag=True)
@click.option('--from-date', type=str, help='Start date: mm/dd/yyyy')
@click.option('--to-date', type=str, help='End date: mm/dd/yyyy')
def analyze(file, findcodes, informationalonly, successonly, redirectonly, errorsonly, apache, json, nginx, explain, from_date, to_date):

    if (apache and nginx) or (apache and json) or (json and nginx):
        print("Only one format flag accepted")
        return

    filter_flags = [findcodes, informationalonly, successonly, redirectonly, errorsonly]
    if sum(filter_flags) > 1:
        print("Only one search flag accepted")
        return

    if apache:
        log_format = "apache"
        index = 8
    elif json:
        log_format = "json"
        index = 5
    elif nginx:
        log_format = "nginx"
        index = 8
    else:
        print("Please specify a log format: --apache, --json, or --nginx")
        return

    try:
        lines = read(file)
        from_date, to_date = date_filter(from_date, to_date)
        type, codes = process(lines, index, findcodes, informationalonly, successonly, redirectonly, errorsonly, from_date, to_date, log_format, explain)

        if not findcodes:
            if informationalonly or successonly or redirectonly or errorsonly:
                statement = codes_print(type, codes, explain)
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

def codes_print(type, codes, explain):

    lines = [f"{type} Codes Found:\n"]
    for code, cnt in sorted(codes.items()):
        lines.append(f"{code}: {cnt}")
        if explain:
            explanation = CODE_EXPLANATIONS.get(code, "Unknown code.")
            lines.append(f"{code} - {explanation}\n")

    return "\n".join(lines)

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

    code_counts = {}

    for line in lines:
        if from_date or to_date:
            line_date = parse_line_date(line, log_format)
            if not in_date_range(line_date, from_date, to_date):
                continue

        parts = line.split()
        try:
            code = parts[index]
            if code[0] in ("1", "2", "3", "4", "5"):
                code_counts[code] = code_counts.get(code, 0) + 1

        except IndexError:
            continue

    return code_counts

def filter_by_category(informationalonly, successonly, redirectonly, errorsonly, code_counts):
    if informationalonly:
        return "Informational", {k: v for k, v in code_counts.items() if k[0] == "1"}

    if successonly:
        return "Success", {k: v for k, v in code_counts.items() if k[0] == "2"}

    if redirectonly:
        return "Redirectional", {k: v for k, v in code_counts.items() if k[0] == "3"}

    if errorsonly:
        return "Error", {k: v for k, v in code_counts.items() if k[0] in ("4", "5")}

    return None, {}

def process(lines, index, findcodes, informationalonly, successonly, redirectonly, errorsonly, from_date, to_date, log_format, explain):

    if findcodes or errorsonly or informationalonly or successonly or redirectonly:
        code_counts = count(lines, index, from_date, to_date, log_format)

        if findcodes:
            output = ["Codes Found:\n"]
            for code, cnt in sorted(code_counts.items()):
                output.append(f"{code}: {cnt}")
                if explain:
                    explanation = CODE_EXPLANATIONS.get(code, "Unknown code.")
                    output.append(f"{code} - {explanation}\n")
            print("\n".join(output))

        return filter_by_category(informationalonly, successonly, redirectonly, errorsonly, code_counts)

    return None, {}

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