document.getElementById('registrationForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, age }),
    });

    const data = await response.json();
    document.getElementById('registrationResult').textContent = `Voter ID: ${data.voter_id}`;
});

document.getElementById('votingForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const voterId = document.getElementById('voterId').value;
    const candidate = document.getElementById('candidate').value;

    const response = await fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ voter_id: voterId, candidate }),
    });

    const data = await response.json();
    document.getElementById('votingResult').textContent = data.message;
});

document.getElementById('tallyVotes').addEventListener('click', async function () {
    const response = await fetch('/tally', {
        method: 'GET',
    });

    const data = await response.json();
    document.getElementById('results').textContent = `Alice: ${data.Alice}, Bob: ${data.Bob}, Charlie: ${data.Charlie}`;
});
