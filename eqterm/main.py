from prompt_toolkit import PromptSession, print_formatted_text, HTML
from eqterm import bse
from eqterm.formatters import format_output
import click


@click.group()
def cli():
    pass


cli.add_command(bse.bse)


# @click.command()
# @click.option('-i', default=False)
# @click.option('-i', default=False)
# def top():
#
#
#

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
