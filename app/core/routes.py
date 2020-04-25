from flask import request, render_template
from app.core import core_bp
from app.services import PreImageService, KNNService, SudokuSolverService


@core_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('pages/index.html')
    if request.method == 'POST':
        file = request.files.get('file').read()
        numbers = PreImageService(file).pre_numbers()
        grid = KNNService.predict(numbers, '/../ml_models/knn.sav')
        SudokuSolverService.solve(grid)
        return render_template('pages/answer.html', grid=grid)
