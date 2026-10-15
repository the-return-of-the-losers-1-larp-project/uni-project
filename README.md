# uni-project

1. Purpose and main user requirements:
Context. A web shop that sells tickets loses giveaway tickets to bots, leaving human customers empty-handed. The current blocking rules rely heavily on country and IP address, which can also block legitimate customers who are travelling.

Purpose. The app helps the shop’s anti-abuse team (1) see which interaction patterns are associated with automated activity and (2) check whether a live session looks automated, without relying on country or IP address.
User group. Anti-abuse analysts at the web shop.

Key user questions.
Which interaction patterns (e.g. click timing, mouse path curvature, typing speed) differ most between bot and human sessions?
Do bot sessions differ by referrer type or other session data?
Is this live session a bot or a human, and which past sessions does it resemble?


1. The system shall allow users to run SQL queries on the data.
2. The system shall return human-or-bot verdict and show the three most similar historical sessions with their labels.
3. The system shall use a trained classification model to display a human-or-bot verdict for the entered session.
4. The system shall display the average value of each interaction metric for bot sessions and for human sessions in a table.
5. The system shall allow users to filter the recorded sessions by label, referrer type and session duration.

6. Dataset description:
The dataset (08_bot_vs_human.csv) holds 400 web shop sessions recorded by the shop’s anti-abuse team, one row per session.
Target: bot (1 = confirmed automated, 0 = human).
Features:
mouse behaviour: clicks, intervals between clicks, path curvature;
keyboard behaviour: digraph latency, dwell time on three form fields;
activity patterns: idle ratio, scroll entropy;
session metadata: timezone mismatch, referrer type, viewport width.





7. Planned queries and outputs:





8. Intended ML outcome:
The system shall output either 0(human user) or 1(bot user)







