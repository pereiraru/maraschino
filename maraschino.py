from flask import Flask, jsonify, render_template, request
from database import db_session
import hashlib, json, jsonrpclib, urllib

app = Flask(__name__)

from settings import *
from noneditable import *
from tools import *

from applications import *
from controls import *
from currently_playing import *
from diskspace import *
from library import *
from recently_added import *
from sabnzbd import *
from trakt import *

from modules import *
from models import Module, Setting

@app.route('/')
@requires_auth
def index():
    unorganised_modules = Module.query.order_by(Module.position)
    modules = [[],[],[]]

    for module in unorganised_modules:
        module_info = get_module_info(module.name)
        module.template = '%s.html' % (module.name)
        module.static = module_info['static']
        modules[module.column - 1].append(module)

    fanart_backgrounds = get_setting_value('fanart_backgrounds') == '1'

    applications = []

    try:
        applications = Application.query.order_by(Application.position)

    except:
        pass

    return render_template('index.html',
        modules = modules,
        show_currently_playing = True,
        fanart_backgrounds = fanart_backgrounds,
        applications = applications,
        show_tutorial = unorganised_modules.count() == 0,
    )

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, port=PORT, host='0.0.0.0')
