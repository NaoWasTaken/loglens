import click

@click.command()
@click.argument('name')
@click.option('--uppercase', is_flag=True)
def test(name, uppercase):
    message = f"Hello, {name}!"
    if uppercase == True:
        print(message.upper())
    else:
        print(message)

if __name__ == "__main__":
    test()