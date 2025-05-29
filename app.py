import cherrypy
from models import *
import os

TEMPLATE_DIR = os.path.join(os.path.abspath("."), "templates")


class VisitApp:
    @cherrypy.expose
    def index(self):
        # Выбираем посещения, присоединяя Пациента и Врача
        visits = Visit.select().join(Patient).switch(Visit).join(Doctor)

        html = open(os.path.join(TEMPLATE_DIR, 'index.html'), encoding='utf-8').read()
        rows = ""
        arows = ''
        for v in visits:
            rows += f"""
            <tr>
                <td>{v.visit_id}</td>
                <td>{v.patient.name}</td>
                <td>{v.doctor.name}</td>
                <td>{v.reason}</td>
                <td>{v.duration}</td>
            </tr>
            """
        return html.replace("{{rows}}", rows)

    @cherrypy.expose
    def add(self, **kwargs):
        if kwargs:
            visit_id = int(kwargs['visit_id'])
            patient_name = kwargs['patient']
            doctor_name = kwargs['doctor']
            reason = kwargs['reason']
            duration = int(kwargs['duration'])

            # Автоматическое создание пациента и врача, если их нет
            patient, _ = Patient.get_or_create(name=patient_name)
            doctor, _ = Doctor.get_or_create(name=doctor_name)

            # Создание посещения
            Visit.create(
                visit_id=visit_id,
                patient=patient,
                doctor=doctor,
                reason=reason,
                duration=duration
            )
            raise cherrypy.HTTPRedirect("/")
        else:
            html = open(os.path.join(TEMPLATE_DIR, 'add_visit.html'), encoding='utf-8').read()
            return html


if __name__ == '__main__':
    # Создаем таблицы и тестовые данные
    create_tables()

    # Запуск сервера
    conf = {
        '/': {
            'tools.staticdir.root': TEMPLATE_DIR
        }
    }

    cherrypy.quickstart(VisitApp(), '/', conf)
