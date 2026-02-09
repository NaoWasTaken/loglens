def read(target):
    lines = []
    with open(target) as sample:
        for i in sample:
            lines.append(i)

    return lines

def parse(lines):
    code_200 = 0
    code_404 = 0
    code_500 = 0

    for _ in lines:
        codes = _.split()
        if codes[8] == "200":
            code_200 +=1
        elif codes[8] == "404":
            code_404 +=1
        elif codes[8] == "500":
            code_500 +=1
        else:
            print("Unable to ascertain codes.")
            exit
    
    print(f"Users encountered {code_200} 200 Status Codes, {code_404} 404 Status Codes, and {code_500} 500 Status Codes.")

def main():
    file = input("Enter File Name: ").lower()
    lines = read(file)
    parse(lines)


if __name__ == "__main__":
    main()