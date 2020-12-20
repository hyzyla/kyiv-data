from flask import Blueprint, render_template

blueprint = Blueprint(
    name="docs",
    import_name=__name__,
    url_prefix="/docs",
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/')
def get_docs():
    print('sending docs')
    return render_template('index.html')
