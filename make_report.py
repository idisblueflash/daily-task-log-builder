

import click

from services import DemoLogReader


@click.command()
@click.argument('file_name')
@click.option('--daily', default=True, help='Only show the latest daily')
@click.option('--email', default=False, help='Show email messages')
@click.option('--excel', default=False, help='generate execle output file')
def make(file_name, daily, email, excel):
    reader = DemoLogReader(file_name)
    reader.daily = daily
    reader.parse()
    reader.report()
    if excel:
        reader.save_excel()
    if email:
        reader.print_email()


if __name__ == '__main__':
    make()
