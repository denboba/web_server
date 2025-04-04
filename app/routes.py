"""write doc here"""
import logging
import os
from flask import request, jsonify
from app import webserver

# Example endpoint definition
logger = logging.getLogger('webserver')


def get_next_job_id():
    """this function returns the next job id"""
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    return job_id


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """"this function returns the results"""
    logger.info('Get results for job_id: %s', job_id)

    if not webserver.tasks_runner.is_job_done(job_id):
        return jsonify({'status': 'running'})
    result = webserver.tasks_runner.get_job_result(job_id)
    if result is None:
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})

    return jsonify({'status': 'done', 'data': result})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """method to request states mean"""
    data = request.json
    logger.info('States mean request: %s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.states_mean,
        data['question']
    )
    return jsonify({'job_id': job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """function to request state mean"""
    data = request.json
    logger.info('State mean request %s', data)

    if 'question' not in data or 'state' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question or state parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.state_mean,
        data['question'],
        data['state']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """function to request best5 states"""
    data = request.json
    logger.info('Best5 request: %s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.best5,
        data['question']
    )
    return jsonify({'job_id': job_id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """function to request worst5 states"""
    data = request.json
    logger.info('Worst5 request %s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.worst5,
        data['question']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """"function to request global mean"""
    data = request.json
    logger.info('Global mean request %s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.global_mean,
        data['question']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """function to request diff from mean"""
    data = request.json
    logger.info('Diff from mean request:%s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.diff_from_mean,
        data['question']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """function to request state diff from mean"""
    data = request.json
    logger.info('State diff from mean request: %s', data)

    if 'question' not in data or 'state' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question or state parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.state_diff_from_mean,
        data['question'],
        data['state']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """function to request mean by category"""
    data = request.json
    logger.info('Mean by category request :%s', data)

    if 'question' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.mean_by_category,
        data['question']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """function to request state mean by category state"""
    data = request.json
    logger.info('State mean by category request: %s', data)

    if 'question' not in data or 'state' not in data:
        return jsonify({
            'status': 'error',
            'reason': 'Missing question or state parameter'
        })

    job_id = get_next_job_id()
    webserver.tasks_runner.add_task(
        job_id,
        webserver.data_ingestor.state_mean_by_category,
        data['question'],
        data['state']
    )

    return jsonify({'job_id': job_id})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """"function for graceful shutdown"""
    logger.info('Graceful shutdown requested')
    webserver.tasks_runner.graceful_shutdown()

    if not webserver.tasks_runner.job_queue.empty():
        return jsonify({'status': 'running'})

    return jsonify({'status': 'done'})


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """provides status of all jobs"""
    logger.info('Jobs status requested')

    # List all files in results directory
    job_files = [f for f in os.listdir('results') if f.endswith('.json')]
    job_statuses = [{
        f.replace('.json', ''): 'done'
    } for f in job_files]

    return jsonify({
        'status': 'done',
        'data': job_statuses
    })


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """provides number of jobs in queue"""
    logger.info('Number of jobs requested')
    return jsonify({'num_jobs': webserver.tasks_runner.job_queue.qsize()})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """function for index page"""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    """"function to get defined routes"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
