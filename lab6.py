import os
import pandas as pd
import cherrypy
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

DATA_FILE = 'data.csv'
COLUMNS = ['id', 'patient_name', 'doctor_name', 'reason', 'duration', 'date']


class DataManager:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                df = pd.read_csv(DATA_FILE, dtype={'id': int})
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                return df
            except:
                return pd.DataFrame(columns=COLUMNS)
        return pd.DataFrame(columns=COLUMNS)

    def save_data(self):
        self.df.to_csv(DATA_FILE, index=False)

    def get_next_id(self):
        return self.df['id'].max() + 1 if not self.df.empty else 1

    def get_visit(self, visit_id):
        visit = self.df[self.df['id'] == visit_id]
        return visit.iloc[0].to_dict() if not visit.empty else None

    def add_visit(self, data):
        new_row = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.save_data()

    def update_visit(self, visit_id, data):
        idx = self.df.index[self.df['id'] == visit_id].tolist()
        if idx:
            for key, value in data.items():
                self.df.at[idx[0], key] = value
            self.save_data()
            return True
        return False

    def delete_visit(self, visit_id):
        self.df = self.df[self.df['id'] != visit_id]
        self.save_data()


class ClinicWeb:
    def __init__(self):
        self.data_manager = DataManager()
        self.templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
        self.initialize_templates()
        self.env = Environment(loader=FileSystemLoader(self.templates_dir, encoding='utf-8'))

    def initialize_templates(self):
        if not os.path.exists('templates'):
            os.makedirs('templates')

        # Принудительно перезаписываем все шаблоны
        templates = {
            'base.html': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Поликлиника{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .nav { margin-bottom: 20px; padding: 10px; background: #f8f8f8; }
        .nav a { margin-right: 15px; text-decoration: none; color: #333; }
        .nav a:hover { color: #0066cc; }
        .btn { padding: 5px 10px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .btn:hover { background: #45a049; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: inline-block; width: 150px; }
        .form-group input, .form-group select { padding: 5px; width: 300px; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Главная</a>
        <a href="/visits">Посещения</a>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>''',

            'index.html': '''{% extends "base.html" %}
{% block content %}
    <h1>Система учета посещений</h1>
    <p>Добро пожаловать! Используйте меню для работы с данными.</p>
{% endblock %}''',

            'visits.html': '''{% extends "base.html" %}
{% block title %}Посещения{% endblock %}
{% block content %}
    <h1>Список посещений</h1>
    <a href="/visits/add" class="btn">➕ Добавить новое</a>
    <table>
        <tr>
            <th>ID</th>
            <th>Пациент</th>
            <th>Врач</th>
            <th>Причина</th>
            <th>Длительность</th>
            <th>Дата</th>
            <th>Действия</th>
        </tr>
        {% for visit in visits %}
        <tr>
            <td>{{ visit.id }}</td>
            <td>{{ visit.patient_name }}</td>
            <td>{{ visit.doctor_name }}</td>
            <td>{{ visit.reason }}</td>
            <td>{{ visit.duration }} мин</td>
            <td>{{ visit.date }}</td>
            <td>
                <a href="/visits/edit/{{ visit.id }}" title="Редактировать">✏️</a>
                <a href="/visits/delete/{{ visit.id }}" title="Удалить">❌</a>
            </td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}''',

            'visit_form.html': '''{% extends "base.html" %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
    <h1>{{ title }}</h1>
    <form method="post">
        <div class="form-group">
            <label for="patient_name">ФИО пациента:</label>
            <input type="text" name="patient_name" id="patient_name" 
                   value="{{ visit.patient_name if visit }}" required>
        </div>

        <div class="form-group">
            <label for="doctor_name">ФИО врача:</label>
            <input type="text" name="doctor_name" id="doctor_name" 
                   value="{{ visit.doctor_name if visit }}" required>
        </div>

        <div class="form-group">
            <label for="reason">Причина обращения:</label>
            <input type="text" name="reason" id="reason" 
                   value="{{ visit.reason if visit }}" required>
        </div>

        <div class="form-group">
            <label for="duration">Длительность (минут):</label>
            <input type="number" name="duration" id="duration" 
                   value="{{ visit.duration if visit else 15 }}" min="1" required>
        </div>

        <div class="form-group">
            <label for="date">Дата приема:</label>
            <input type="date" name="date" id="date" 
                   value="{{ visit.date if visit else today }}" required>
        </div>

        <button type="submit" class="btn">💾 Сохранить</button>
    </form>
{% endblock %}'''
        }

        for filename, content in templates.items():
            filepath = os.path.join('templates', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    def render_template(self, template_name, **kwargs):
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:
            return f"Ошибка шаблона: {str(e)}"

    @cherrypy.expose
    def index(self):
        return self.render_template('index.html')

    @cherrypy.expose
    def visits(self, *args, **kwargs):
        visits = self.data_manager.df.astype(str).to_dict('records')
        return self.render_template('visits.html', visits=visits)

    @cherrypy.expose
    def visits_add(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return self.render_template('visit_form.html',
                                    title="Новое посещение",
                                    today=today)

    @cherrypy.expose
    def visits_edit(self, visit_id):
        try:
            visit_id = int(visit_id)
            visit = self.data_manager.get_visit(visit_id)
            if not visit:
                raise ValueError

            today = datetime.now().strftime('%Y-%m-%d')
            return self.render_template('visit_form.html',
                                        title="Редактирование",
                                        visit=visit,
                                        today=today)
        except:
            raise cherrypy.HTTPError(404, "Запись не найдена")

    @cherrypy.expose
    def visits_delete(self, visit_id):
        try:
            self.data_manager.delete_visit(int(visit_id))
        except:
            pass
        raise cherrypy.HTTPRedirect("/visits")

    @cherrypy.expose
    def visits_update(self, visit_id=None, **kwargs):
        if cherrypy.request.method == 'POST':
            try:
                data = {
                    'patient_name': kwargs.get('patient_name', '').strip(),
                    'doctor_name': kwargs.get('doctor_name', '').strip(),
                    'reason': kwargs.get('reason', '').strip(),
                    'duration': int(kwargs.get('duration', 15)),
                    'date': kwargs.get('date', ''),
                    'id': int(visit_id) if visit_id else self.data_manager.get_next_id()
                }

                # Валидация данных
                if not all([data['patient_name'], data['doctor_name'], data['reason']]):
                    raise ValueError("Все поля обязательны для заполнения")

                if visit_id:
                    if not self.data_manager.update_visit(data['id'], data):
                        raise ValueError
                else:
                    self.data_manager.add_visit(data)

            except Exception as e:
                print(f"Ошибка: {str(e)}")
                raise cherrypy.HTTPRedirect("/visits")

            raise cherrypy.HTTPRedirect("/visits")


if __name__ == '__main__':
    # Очистка старых данных (раскомментировать при первом запуске)
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    if os.path.exists('templates'):
        import shutil
         shutil.rmtree('templates')

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload.on': True
    })

    cherrypy.quickstart(ClinicWeb(), '/', conf)