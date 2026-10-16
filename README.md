# uni-project

## Purpose and main user requirements:

### Context.
A web shop that sells tickets loses giveaway tickets to bots, leaving human customers empty-handed. The current blocking rules rely heavily on country and IP address, which can also block legitimate customers who are travelling.

### Purpose.
The app helps the shop’s anti-abuse team
1) see which interaction patterns are associated with automated activity and 
2) check whether a live session looks automated, without relying on country or IP address.

### User group.
Anti-abuse analysts at the web shop.

### Key user questions.
- Which interaction patterns (e.g. click timing, mouse path curvature, typing speed) differ most between bot and human sessions?
- Do bot sessions differ by referrer type or other session data?
- Is this live session a bot or a human, and which past sessions does it resemble?

### The system shall...
1. ...allow users to run SQL queries on the data.
2. ...return human-or-bot verdict and show the three most similar historical sessions with their labels.
3. ...use a trained classification model to display a human-or-bot verdict for the entered session.
4. ...display the average value of each interaction metric for bot sessions and for human sessions in a table.
5. ...allow users to filter the recorded sessions by label, referrer type and session duration.

### Dataset description:
The dataset (08_bot_vs_human.csv) holds 400 web shop sessions recorded by the shop’s anti-abuse team, one row per session.
Target: bot (1 = confirmed automated, 0 = human).

Features:
- mouse behaviour: clicks, intervals between clicks, path curvature;
- keyboard behaviour: digraph latency, dwell time on three form fields;
- activity patterns: idle ratio, scroll entropy;
- session metadata: timezone mismatch, referrer type, viewport width.

### Planned queries and outputs:
Average of each interaction metric, grouped by label.
Sessions filtered by duration, label and referrer type.

OUTPUTS:
- A filterable table of sessions
- A distribution chart of a selected metric, split by label.
- A comparison table of average metrics for bots and humans.

For a live session: a verdict and the three most similar historical sessions with labels


### Intended ML outcome:
The system shall output either 0(human user) or 1(bot user)
- Task: binary classification of a session as bot or human.
- Output for the user: a verdict plus the three most similar historical sessions
(nearest neighbours) with their labels. The choice of algorithm will be made in the design phase.








