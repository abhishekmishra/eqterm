from prompt_toolkit import PromptSession, print_formatted_text, HTML
from eqterm.bse import *
from eqterm.formatters import format_output


@click.group()
def cli():
    pass


@click.command()
def bluh():
    click.echo('wut')


cli.add_command(bse)
cli.add_command(bluh)


def main():
    session = PromptSession()

    while True:
        try:
            text = session.prompt('eqterm> ')
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.

        try:
            messages = cli(text.split(), prog_name="blah", standalone_mode=False)
        except Exception as e:
            print(repr(e))
        else:
            if messages is not None:
                text = format_output(messages['obj'], messages['value'])
                print_formatted_text(HTML(text))

    print('GoodBye!')


if __name__ == "__main__":
    main()
