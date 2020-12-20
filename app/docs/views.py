from flask import Blueprint, render_template

from app.lib.config import settings

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


@blueprint.route('/spec.yaml')
def get_spec():
    return render_template(
        'openapi.yaml',
        server=settings.SERVER_URL,
    )
