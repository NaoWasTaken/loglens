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
        with open(file) as fd:
            lines = []
            for line in fd:
                lines.append(line)
        
        code_1xx = 0
        code_2xx = 0
        code_3xx = 0
        code_4xx = 0
        code_5xx = 0

        if apache:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                for _ in lines:
                    codes = _.split()
                    if findcodes or informationalonly:
                        if codes[8][0] == "1":
                            code_1xx +=1
                    if findcodes or successonly:
                        if codes[8][0] == "2":
                            code_2xx +=1
                    if findcodes or redirectonly:
                        if codes[8][0] == "3":
                            code_3xx +=1
                    if findcodes or errorsonly:
                        if codes[8][0] == "4":
                            code_4xx +=1
                        if codes[8][0] == "5":
                            code_5xx +=1
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    print(f"Informational Codes Found: 1xx - {code_1xx}")

                if successonly:
                    print(f"Success Codes Found: 2xx - {code_2xx}")

                if redirectonly:
                    print(f"Redirection Codes Found: 3xx - {code_3xx}")

                if errorsonly:
                    print(f"Errors Found: 4xx - {code_4xx}; 5xx - {code_5xx}")
        
        elif json:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                for _ in lines:
                    codes = _.split()
                    if findcodes or informationalonly:
                        if codes[5][0] == "1":
                            code_1xx +=1
                    if findcodes or successonly:
                        if codes[5][0] == "2":
                            code_2xx +=1
                    if findcodes or redirectonly:
                        if codes[5][0] == "3":
                            code_3xx +=1
                    if findcodes or errorsonly:
                        if codes[5][0] == "4":
                            code_4xx +=1
                        if codes[5][0] == "5":
                            code_5xx +=1
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    print(f"Informational Codes Found: 1xx - {code_1xx}")

                if successonly:
                    print(f"Success Codes Found: 2xx - {code_2xx}")

                if redirectonly:
                    print(f"Redirection Codes Found: 3xx - {code_3xx}")

                if errorsonly:
                    print(f"Errors Found: 4xx - {code_4xx}; 5xx - {code_5xx}")

        elif nginx:
            if findcodes or errorsonly or informationalonly or successonly or redirectonly:
                for _ in lines:
                    codes = _.split()
                    if findcodes or informationalonly:
                        if codes[8][0] == "1":
                            code_1xx +=1
                    if findcodes or successonly:
                        if codes[8][0] == "2":
                            code_2xx +=1
                    if findcodes or redirectonly:
                        if codes[8][0] == "3":
                            code_3xx +=1
                    if findcodes or errorsonly:
                        if codes[8][0] == "4":
                            code_4xx +=1
                        if codes[8][0] == "5":
                            code_5xx +=1
                
                if findcodes:
                    print(f"Codes Found: 1xx - {code_1xx}; 2xx - {code_2xx}; 3xx - {code_3xx}; 4xx - {code_4xx}; 5xx - {code_5xx}")

                if informationalonly:
                    print(f"Informational Codes Found: 1xx - {code_1xx}")

                if successonly:
                    print(f"Success Codes Found: 2xx - {code_2xx}")

                if redirectonly:
                    print(f"Redirection Codes Found: 3xx - {code_3xx}")

                if errorsonly:
                    print(f"Errors Found: 4xx - {code_4xx}; 5xx - {code_5xx}")

    except FileNotFoundError:
        print(f"Error: Could not find file '{file}'")

    except PermissionError:
        print(f"Error: No permission to read '{file}'")

    except Exception as e:
        print(f"An unexpected error occured: {e}")

if __name__ == "__main__":
    analyze()