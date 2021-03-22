import flask
from main import not_found
from data.__all_models import Jobs
from data import db_session

blueprint = flask.Blueprint(
    'job',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).all()
    return flask.jsonify({'jobs': [elm.to_dict() for elm in data]})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        if not flask.request.json:
            return flask.jsonify({'error': 'Empty request'})
        elif not all(key in flask.request.json for key in
                     ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
            return flask.jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        job_id = db_sess.query(Jobs).get(flask.request.json['id'])
        if job_id:
            return flask.jsonify({'error': 'Id already exists'})
        job = Jobs(
                id=flask.request.json['id'],
                team_leader=flask.request.json['team_leader'],
                job=flask.request.json['job'],
                work_size=flask.request.json['work_size'],
                collaborators=flask.request.json['collaborators'],
                is_finished=flask.request.json['is_finished']
        )
        db_sess.add(job)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
    except BaseException as error:
        with open("logs/api.txt", "w") as file:
            file.write(error)


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def redo_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return flask.jsonify({'error': 'Not found'})
    elif not all(key in flask.request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    job.team_leader = flask.request.json['team_leader']
    job.job = flask.request.json['job']
    job.work_size = flask.request.json['work_size']
    job.collaborators = flask.request.json['collaborators']
    job.is_finished = flask.request.json['is_finished']
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    try:
        db_sess = db_session.create_session()
        data = db_sess.query(Jobs).get(job_id)
        return flask.jsonify({f'job[{job_id}]': data.to_dict()})
    except AttributeError:
        return not_found("job with such id didn't found")
