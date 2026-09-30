# Voting System

A small Flask web app for registering voters, casting votes, and tallying results, with each vote stored as a salted SHA-256 hash instead of a plain candidate name.

## Features

- **Voter registration**: each voter gets a unique, randomly generated 8-character voter ID.
- **One person, one vote**: a voter ID can vote only once; a second attempt is rejected.
- **Hashed ballots**: each vote is stored as `sha256(candidate + salt)` with a fresh random salt, so the stored ballot list doesn't contain candidate names in plain text.
- **Live tally**: results are computed by re-hashing each candidate with the ballot's salt and counting matches.
- **Simple web UI**: register, vote, and tally from one page.

## Getting started

Requires Python 3.9+.

```bash
git clone https://github.com/Charannagadeep/Voting-system.git
cd Voting-system/Catalog
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000, register a voter, copy the voter ID, cast a vote, then click **Tally Votes**. Set `FLASK_DEBUG=1` to run in debug mode during development.

## API

| Method | Endpoint | Body | Response |
|---|---|---|---|
| `POST` | `/register` | `{"name": "Ana", "age": 25}` | `{"voter_id": "aB3xK9pQ"}` |
| `POST` | `/vote` | `{"voter_id": "aB3xK9pQ", "candidate": "Alice"}` | `{"message": "Vote cast successfully!"}` |
| `GET` | `/tally` | none | `{"Alice": 2, "Bob": 1, "Charlie": 0}` |

## Project structure

```
Voting-system/
└── Catalog/
    ├── app.py              # Flask routes, VoterRegistry, VotingSystem
    ├── requirements.txt
    ├── templates/index.html
    └── static/             # styles.css, scripts.js
```

## Limitations

This is a learning project, not a production election system:

- Data lives in memory and resets when the server restarts.
- Hashing hides candidate names at rest, but with only three candidates a ballot can be reversed by trying each one. Real systems use techniques such as homomorphic encryption or mix-nets.
- Voter IDs aren't tied to verified identities, and there's no authentication or rate limiting.
