from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from agents.team_agents import initialize_agents, run_team

# Initialize agents once
agents = initialize_agents()

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/ask', methods=['POST'])
@cross_origin()
def ask_endpoint():
    """Endpoint for handling queries"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing query parameter"}), 400
    
    query = data['query']
    try:
        response = run_team(query, agents)
        return jsonify({
            "query": query,
            "response": response
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500