import os
import click
# the commands below need to imported in the microblog.py in the top-level dir


# docstrings are used as help messages in the --help output
def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    # Click passes the lang value provided in the command to the handler function
    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    # commands are confirmed to return 0, which implies no errors
    # decorators are derived from the parent function above
    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages"""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')
