from flask import Flask, render_template, request, jsonify
from hashlib import sha256
import os
import secrets
import string

app = Flask(__name__)

# Helper functions
def create_salt():
    return secrets.token_hex(8)

def hash_data(data, salt):
    return sha256((data + salt).encode()).hexdigest()

# User registration and storage
class VoterRegistry:
    def __init__(self):
        self.voters = {}
    
    def register_voter(self, name, age):
        voter_id = self.generate_voter_id()
        self.voters[voter_id] = {
            'name': name,
            'age': age,
            'voted': False
        }
        return voter_id
    
    def generate_voter_id(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            voter_id = ''.join(secrets.choice(alphabet) for _ in range(8))
            if voter_id not in self.voters:
                return voter_id
    
    def validate_voter(self, voter_id):
        return voter_id in self.voters and not self.voters[voter_id]['voted']
    
    def mark_voted(self, voter_id):
        if self.validate_voter(voter_id):
            self.voters[voter_id]['voted'] = True
            return True
        return False

# Voting system
class VotingSystem:
    def __init__(self):
        self.candidates = ["Alice", "Bob", "Charlie"]
        self.votes = []
    
    def cast_vote(self, voter_id, candidate, voter_registry):
        if candidate not in self.candidates:
            return False
        
        if not voter_registry.validate_voter(voter_id):
            return False
        
        salt = create_salt()
        hashed_vote = hash_data(candidate, salt)
        self.votes.append((hashed_vote, salt))
        
        voter_registry.mark_voted(voter_id)
        return True
    
    def tally_votes(self):
        tally = {candidate: 0 for candidate in self.candidates}
        
        for hashed_vote, salt in self.votes:
            for candidate in self.candidates:
                if hashed_vote == hash_data(candidate, salt):
                    tally[candidate] += 1
                    break
        
        return tally

voter_registry = VoterRegistry()
voting_system = VotingSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    age = data['age']
    voter_id = voter_registry.register_voter(name, age)
    return jsonify({'voter_id': voter_id})

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    voter_id = data['voter_id']
    candidate = data['candidate']
    success = voting_system.cast_vote(voter_id, candidate, voter_registry)
    if success:
        return jsonify({'message': 'Vote cast successfully!'})
    return jsonify({'message': 'Invalid voter ID or candidate.'})

@app.route('/tally', methods=['GET'])
def tally():
    results = voting_system.tally_votes()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
