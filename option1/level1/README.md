# Level 1

🙌 Welcome to the first level 🙌

Let's get started! 🏃‍♀️🏃‍♀️

Given a list of time slots and their corresponding judges, return the total number of judges who judge in at least two or more time slots.

Things to keep in mind:

-   Every time slot will only have one judge
-   Some judges will be judging in more than one time slot

**Get your input at https://inputs.vandyhacks.dev/**

### Details

**Input:** A list of JSON objects where each object represents a judging session (team, judge, time).

```JSON
//an example of an input
[
  {
    "judge": "Daniel Balasubramaniam",
    "team": "Team VandyHacks",
    "time": "2022-10-23T11:20:00.000Z",
  },
  {
    "judge": "Graham Hemingway",
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

**Output:** The total number of judges who judge in at least two or more time slots (in this example, your output would be 1 because only Dr. B judged at two time slots).

### Answer Format

Paste your number into `judges.txt` file in this folder with nothing else (no tabs, spaces, units, etc.)
