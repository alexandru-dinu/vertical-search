# Vertical Search

Vertical Search for Research Papers.

### Example queries

See [Whoosh query language](https://whoosh.readthedocs.io/en/latest/querylang.html).

#### date range + inexact terms
```
>>> Specify (or skip)  paper_field: lg
>>> Specify (or skip)         date: [2014 to 2016]
>>> Specify (or skip)        title: machine translation
>>> Specify (or skip)      authors: bahdanau
>>> Specify (or skip)     abstract: joint* OR align*
```

#### date range + position information
```
>>> Specify (or skip)  paper_field: 
>>> Specify (or skip)         date: [201801 to 201812]
>>> Specify (or skip)        title: 
>>> Specify (or skip)      authors: 
>>> Specify (or skip)     abstract: "swarm collective"~5
```

#### date range + complex boolean
```
>>> Specify (or skip)  paper_field: lg
>>> Specify (or skip)         date: [2018 to 2019]
>>> Specify (or skip)        title: neural OR network
>>> Specify (or skip)      authors: 
>>> Specify (or skip)     abstract: reinforce* NOT (learn* OR agent?)
```