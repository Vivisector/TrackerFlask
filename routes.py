from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Task

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    tasks = Task.query.all()  # Получаем все задачи
    return render_template('index.html', tasks=tasks)

# Страница для создания новой задачи
@bp.route('/task/new', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        progress = request.form.get('progress', 0)  # Получаем прогресс, по умолчанию 0

        task = Task(
            title=title,
            description=description,
            progress=progress  # Убедимся, что значение — это число
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('routes.index'))  # Возврат на главную страницу
    return render_template('create_task.html')

# Страница для редактирования задачи
@bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)  # Получаем задачу по ID или выводим 404
    if request.method == 'POST':
        # Обновляем данные задачи
        task.title = request.form['title']
        task.description = request.form['description']
        task.status = request.form.get('status', 'pending')
        db.session.commit()
        return redirect(url_for('routes.index'))  # Возврат на главную страницу
    return render_template('edit_task.html', task=task)

# Страница для завершения задачи
@bp.route('/task/complete/<int:id>', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.status = 'done'
    db.session.commit()
    return redirect(url_for('index'))

# Страница для удаления задачи
@bp.route('/task/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))