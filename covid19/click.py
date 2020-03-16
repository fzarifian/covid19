import click
import json
from .models import CollectionFactory, Collection

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


@cli.command()
@click.argument('file', type=click.File('r'))
@click.pass_context
def data(ctx, file):
    collections = CollectionFactory()

    for entity in json.load(file):
        collections.add(entity)
    
    click.echo(collections.to_json())

@cli.command()
@click.argument('file', type=click.File('r'))
@click.pass_context
def export(ctx, file):
    collections = CollectionFactory()

    for entity in json.load(file):
        collections.add(entity)

if __name__ == '__main__':
    cli(obj={})
