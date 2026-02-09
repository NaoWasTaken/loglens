import click

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
def analyze(file, findcodes, informationalonly, successonly, redirectonly, errorsonly, apache, json, nginx):
    try:
        lines = read(file)

        if apache:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                code_1xx, code_2xx, code_3xx, code_4xx, code_5xx = count(lines, 8)
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    type = "Informational"
                    code_xx = code_1xx

                if successonly:
                    type = "Success"
                    code_xx = code_2xx

                if redirectonly:
                    type = "Redirection"
                    code_xx = code_3xx

                if errorsonly:
                    type = "Error"
                    code_xx = code_4xx + code_5xx
        
        elif json:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                code_1xx, code_2xx, code_3xx, code_4xx, code_5xx = count(lines, 5)
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    type = "Informational"
                    code_xx = code_1xx

                if successonly:
                    type = "Success"
                    code_xx = code_2xx

                if redirectonly:
                    type = "Redirection"
                    code_xx = code_3xx

                if errorsonly:
                    type = "Error"
                    code_xx = code_4xx + code_5xx

        elif nginx:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                code_1xx, code_2xx, code_3xx, code_4xx, code_5xx = count(lines, 8)
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    type = "Informational"
                    code_xx = code_1xx

                if successonly:
                    type = "Success"
                    code_xx = code_2xx

                if redirectonly:
                    type = "Redirection"
                    code_xx = code_3xx

                if errorsonly:
                    type = "Error"
                    code_xx = code_4xx + code_5xx

        if not findcodes:
            if informationalonly or successonly or redirectonly or errorsonly:
                statement = codes_print(type, code_xx)
                print(statement)

    except FileNotFoundError:
        print(f"Error: Could not find file '{file}'")

    except PermissionError:
        print(f"Error: No permission to read '{file}'")

    except Exception as e:
        print(f"An unexpected error occured: {e}")

def read(file):
    with open(file) as fd:
        lines = []
        for line in fd:
            lines.append(line)

    return lines

def codes_print(type, code):
    statement = f"{type} Codes Found - {code}"
    
    return statement

def count(lines, index):

    code_1xx = 0
    code_2xx = 0
    code_3xx = 0
    code_4xx = 0
    code_5xx = 0

    for _ in lines:
        codes = _.split()
        if codes[index][0] == "1":
            code_1xx +=1
        if codes[index][0] == "2":
            code_2xx +=1
        if codes[index][0] == "3":
            code_3xx +=1
        if codes[index][0] == "4":
            code_4xx +=1
        if codes[index][0] == "5":
            code_5xx +=1

    return code_1xx, code_2xx, code_3xx, code_4xx, code_5xx

def get_type():
    pass


if __name__ == "__main__":
    analyze()