import click
import os
import sys
import github


@click.group()
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def root(ctx, debug):
    try:
        ctx.ensure_object(dict)
    except Exception as e:
        click.echo(
            "Unable to initialize context with the folllowing error:\n%s" % e)
    if debug:
        click.echo('Debugging is turned on.')
    ctx.obj['DEBUG'] = debug


@root.command('os')
@click.pass_context
def print_os_info(ctx):
    click.echo("""Current Directory: %s\
        \nCurrent Directory: %s\
    """ % (
        os.path.abspath('.'),
        os.path.abspath('.')
    ))
    click.echo('Platform: %s' % os.name)
    click.echo('File System Encoding: %s' % sys.getdefaultencoding())


@root.command('env')
@click.option('--pretty', '-p', is_flag=True, help='Pretty print multi-value variables', default=False)
@click.option('--file', '-f', help='Write output to file', default=None)
@click.pass_context
def print_env(ctx, pretty, file):
    if ctx.obj['DEBUG']:
        click.echo("Prettyifying and writing output to %s" % file)
    for key, value in os.environ.items():
        click.echo("%s=%s" % (key, value))


@root.command('github')
@click.option('--name', '-n', prompt='Enter repository name', help='Name of repository to create')
@click.option('--description', '-d', prompt='Enter description', help='Description for repository', default='No description was set for this project.')
@click.option('--private', '-p', is_flag=True, default=False)
@click.pass_context
def create_repo(ctx, name, description, private):
    response = github.create_repo(name, description, private)
    click.echo(message=response.message, err=not response.status)


if __name__ == "__main__":
    root(obj={})
