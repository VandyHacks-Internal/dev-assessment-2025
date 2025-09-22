# Level 3

Glad you've made it this far 🙏

Just one more level before you potentially join the best dev team that has possibly ever existed 🤩 So let's get straight into into it!

Given a list of judging score cards submitted during a make-believe VandyHacks, determine which (if any) teams are tied by `average score` and help us resolve the ties.

**Get your input at https://inputs.vandyhacks.dev/**

### Details

**Input:** A list of judging score cards, where each score card is a JSON object containing the team, the judge, the scores in 5 different categories, and the judge's comments.

```JSON
// Example input with just 3 score cards
[
  {
    "team": "Franecki Inc",
    "judge": "Brenda Rau",
    "technical_ability": 2,
    "creativity": 7,
    "utility": 9,
    "presentation": 6,
    "wow_f_actor": 5,
    "comment": "Sed autem amet voluptas.\nMolestiae laudantium sit velit consectetur harum excepturi qui.\nQuae beatae quidem rem tempore recusandae.\nQuo quod sunt ipsum recusandae ea nihil repellendus ut voluptatem."
  },
  {
    "team": "Schuppe - Jenkins",
    "judge": "Travis Spinka PhD",
    "technical_ability": 6,
    "creativity": 2,
    "utility": 3,
    "presentation": 2,
    "wow_factor": 1,
    "comment": "Voluptas quod ullam autem eum omnis reprehenderit enim reiciendis."
  },
  {
    "team": "Halvorson, Daniel and Windler",
    "judge": "Earnest Daniel",
    "technical_ability": 5,
    "creativity": 2,
    "utility": 6,
    "presentation": 10,
    "wow_factor": 10,
    "comment": "necessitatibus dolorem doloribus"
  }
]
```

For each score card, the team's `total score` is the sum the scores in each of the 5 categories.

Each team's average score is the average of the `total score` given on each score card (i.e. if a team was judged three times the input list will have three score cards associated with that team, so if the score cards had `total score = 37`, `total score = 41`, and `total score = 42`, then that team has `average score = 40`).

Your first task is to compute the `average score` of each team and find out which teams are tied (have the same `average score`).

For each of these teams, we would like to break the tie by adding one additional judging session per team.

For such a judging session, we define a `potential judge` as a judge that has not already judged the team, but _has_ judged one of the teams that the team is tied with.

Your goal is to tell us about all of the ties that exist and give us a list of `potential judge`s for each team that is involved in a tie.

## Answer format

A text file describing all of the ties and potential judges to resolve ties. Please put your output in a file named `ties.txt` in this directory.

```txt
Tie between ['Alvarez-Jordan', 'Brown, Quinn and Baldwin', 'Wilson PLC'] with scores 26

Possible judges for Alvarez-Jordan: ['David Munoz', 'Jessica Bruce', 'Jessica Reyes', 'Richard Alvarez', 'Taylor Burgess', 'Zachary Henson']

Possible judges for Brown, Quinn and Baldwin: ['Brianna Garcia', 'David Thornton', 'Jessica Bruce', 'Patricia Wiley', 'Taylor Burgess', 'Zachary Henson']

Possible judges for Wilson PLC: ['Brianna Garcia', 'David Munoz', 'David Thornton', 'Jessica Reyes', 'Patricia Wiley', 'Richard Alvarez']
---
Tie between ['James Group', 'Villanueva-Robinson'] with scores 25

Possible judges for James Group: ['David Fuller', 'Travis Rocha']

Possible judges for Villanueva-Robinson: ['Brianna Garcia', 'Peggy Mathews MD']
---
Tie between ['Lee-Rodriguez', 'Vasquez-Mcguire'] with scores 22

Possible judges for Lee-Rodriguez: ['David Munoz', 'Jessica Reyes']

Possible judges for Vasquez-Mcguire: ['Jessica Bruce', 'Taylor Burgess']

```

🚨🚨🚨 The format of your output is very important 🚨🚨🚨

For each tie, the first line should be of the format: `Tie between ${teams} with scores ${average score}`

Where `teams` is an array sorted alphabetically and `average score` is either an integer or float rounded to 2 decimal places.

Then for each team, you should output a statement of the following format: `Possible judges for ${team}: ${potential judges}`.

Where `potential judges` is an array sorted alphabetically. Note that this statement should appear in alphabetically order by `team` with empty lines separating each statement.

Finally, the preceding output should appear in descending order of `average score` for the tie, with a `---` line separating each set of ties. Note that each line should also end with a newline character, hence the empty line at the end.
