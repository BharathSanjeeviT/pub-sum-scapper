from flask import Blueprint, json, request, jsonify
from modules import QueueProcessor

blueprint = Blueprint('scrapper', __name__) 
process_queue = QueueProcessor()

@blueprint.route('/scrape-author', methods=['POST'])
def gsindex():
    authors = json.loads(request.data)
    try:
        process_queue.add(authors)
        return jsonify({ 
            'status': 200,
            'message': 'Authors added to queue' 
        })
    except Exception as err:
        return jsonify({
            'status': 400,
            'err': err
        })

@blueprint.route('/shut-the-fcuk-up', methods=['GET'])
def shutdown():
    process_queue.shutdown()
    return jsonify({ 'status': 200, 'message': 'Server shutting down' })

@blueprint.route('/hey', methods=['GET'])
def hello():
    return jsonify({ 'status': 200, 'message': 'HELLO' })
