# Level 2

🙌 Welcome to the second level 🙌

Hope you had a good warm up with the previous challenge, because things are going to get 🎢

Given a list of possible judging schedules, we need to know if each schedule is a `good` schedule.

A schedule is `good` if it satisfies all of the following conditions:

1. No judge is having two sessions at the same time
2. No team is having two sessions at the same time
3. Each team is judged by at least 2 judges
4. Each judge is judging at least 2 teams
5. No judge is judging the same team more than once

You won't be given the number of judges / teams beforehand, but you can assume that all teams and judges will appear at least once in a judging schedule.

**Get your input at https://inputs.vandyhacks.dev/**

### Details

**Input:** A list of judging schedules, or equivalently: a list of list of JSON objects, where each JSON object represents a judging session (team, judge, time).

```JSON
// an example of a bad judging schedule because it violates rule 4
[
  {
    "judge": "Graham Hemingway",
    "team": "Team VandyHacks",
    "time": "2022-10-23T11:20:00.000Z",
  },
  {
    "judge": "Douglas Schmidt",
    "team": "Team ChangePlusPlus",
    "time": "2022-10-23T12:00:00.000Z",
  },
  {
    "judge": "Daniel Balasubramaniam",
    "team": "Team CTF",
    "time": "2022-10-23T10:40:00.000Z",
  },
]

```

**Output:** A list of booleans denoting whether each judging schedule is a `good`.

### Answer Format

Paste your list of booleans into `schedule.json` file in this folder.
Follow this format: `[true, true, true, false, false, true, true]`
