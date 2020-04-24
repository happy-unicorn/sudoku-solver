from flask import request, render_template, redirect, url_for
from app.core import core_bp


@core_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('pages/index.html')
    if request.method == 'POST':
        from random import choice
        array = [[choice(list(range(1, 10))) for _ in range(9)] for _ in range(9)]
        return render_template('pages/answer.html', grid=array)
