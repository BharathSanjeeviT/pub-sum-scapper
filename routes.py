from flask import Blueprint, jsonify, request
from scrapper import get_author_gs
blueprint = Blueprint('scrapper', __name__) 

@blueprint.route('/gsauthor', methods=['GET'])
def index():
    author_id = request.args.get('author_id')
    if author_id:
        return get_author_gs(author_id)
    else:
        return jsonify({ 'status': 400 })
