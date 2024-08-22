import hashlib
import random
import string

# Helper functions
def create_salt():
    """Creates a random salt for hashing."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def hash_data(data, salt):
    """Hashes the data with a salt."""
    return hashlib.sha256((data + salt).encode()).hexdigest()

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
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
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
            print("Invalid candidate.")
            return False
        
        if not voter_registry.validate_voter(voter_id):
            print("Invalid voter ID or voter has already voted.")
            return False
        
        salt = create_salt()
        hashed_vote = hash_data(candidate, salt)
        self.votes.append(hashed_vote)
        
        voter_registry.mark_voted(voter_id)
        return True
    
    def tally_votes(self):
        tally = {candidate: 0 for candidate in self.candidates}
        
        for vote in self.votes:
            for candidate in self.candidates:
                for salt_candidate in [vote[-16:]]:
                    if vote == hash_data(candidate, salt_candidate):
                        tally[candidate] += 1
        
        return tally

# Example usage
voter_registry = VoterRegistry()
voting_system = VotingSystem()

# Registering voters
voter_id_1 = voter_registry.register_voter("John Doe", 30)
voter_id_2 = voter_registry.register_voter("Jane Smith", 25)

# Casting votes
voting_system.cast_vote(voter_id_1, "Alice", voter_registry)
voting_system.cast_vote(voter_id_2, "Bob", voter_registry)

# Tallying the votes
results = voting_system.tally_votes()
print("Voting Results:", results)
