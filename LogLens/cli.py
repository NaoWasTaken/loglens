import click
import sys

@click.command()
@click.argument('file')
@click.option('--findcodes', is_flag=True)
@click.option('--errorsonly', is_flag=True)
@click.option('--apache', is_flag=True)
def analyze(file, findcodes, errorsonly, apache):
    try:
        with open(file) as fd:
            lines = []
            for line in fd:
                lines.append(line)

        code_200 = 0
        code_404 = 0
        code_500 = 0

        if apache:
            if findcodes or errorsonly:
                for _ in lines:
                    codes = _.split()
                    if findcodes:
                        if codes[8] == "200":
                            code_200 +=1
                    elif codes[8] == "404":
                        code_404 +=1
                    elif codes[8] == "500":
                        code_500 +=1
                
                if findcodes:
                    print(f"Codes Found: 200 - {code_200}; 404 - {code_404}; 500 - {code_500}")

                elif errorsonly:
                    print(f"Errors Found: 404 - {code_404}; 500 - {code_500}")

            if not findcodes and not errorsonly:
                print("Successfully Analyzed File")
    except FileNotFoundError:
        print(f"Error: Could not find file '{file}'")

    except PermissionError:
        print(f"Error: No permission to read '{file}'")

    except Exception as e:
        print(f"An unexpected error occured: {e}")

if __name__ == "__main__":
    analyze()