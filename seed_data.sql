PRAGMA foreign_keys = ON;

DELETE FROM votes;
DELETE FROM proposals;
DELETE FROM sqlite_sequence WHERE name IN ('proposals', 'votes');

INSERT INTO proposals (id, title, description, created_at, deadline, status) VALUES
(
    1,
    'Fund the riverside park lights',
    'Install solar path lights along the riverside walk so the park stays usable after dusk.',
    datetime('now', '-1 day'),
    datetime('now', '+5 days'),
    'active'
),
(
    2,
    'Weekly farmers market on Sundays',
    'Close Oak Street for four hours each Sunday for a local producers market.',
    datetime('now', '-2 days'),
    datetime('now', '+2 days'),
    'active'
),
(
    3,
    'Night bus route trial',
    'Run a six-week late bus from the station to the north estates.',
    datetime('now', '-10 days'),
    datetime('now', '-1 day'),
    'expired'
),
(
    4,
    'Rename the community hall',
    'Choose a new name for the hall after the renovation. This proposal was closed by an admin.',
    datetime('now', '-4 days'),
    datetime('now', '+10 days'),
    'closed'
);

INSERT INTO votes (id, proposal_id, voter_name, vote, voted_at) VALUES
(1, 2, 'Amina Shah', 'yes', datetime('now', '-1 day')),
(2, 2, 'Leo Martins', 'yes', datetime('now', '-20 hours')),
(3, 2, 'Priya Nair', 'no', datetime('now', '-5 hours')),
(4, 3, 'Amina Shah', 'yes', datetime('now', '-8 days')),
(5, 3, 'Chris Adeyemi', 'abstain', datetime('now', '-7 days')),
(6, 4, 'Leo Martins', 'no', datetime('now', '-3 days')),
(7, 4, 'Priya Nair', 'no', datetime('now', '-3 days'));
