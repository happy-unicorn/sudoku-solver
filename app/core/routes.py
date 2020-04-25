from flask import request, render_template
import cv2
import numpy as np
from app.core import core_bp


@core_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('pages/index.html')
    if request.method == 'POST':
        file = request.files.get('file').read()
        img = cv2.imdecode(np.fromstring(file, np.uint8), cv2.IMREAD_UNCHANGED)
        return str(img.shape[0]) + " * " + str(img.shape[1])
        # from random import choice
        # array = [[choice(list(range(1, 10))) for _ in range(9)] for _ in range(9)]
        # return render_template('pages/answer.html', grid=array)
