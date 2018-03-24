# What it is 
Finra Challenge 2017: No-Machine-Learning Edition

# The Challenge 
 > Are you ready to become a crime fighter in today’s rapidly growing world of electronic data? Believe it or not, technology can be a super power to help establish relationships between “bad guys” and the people who associate with them. As Superman says, “There is a right and a wrong in the universe, and the distinction is not that hard to make.” Can you identify an entire “gang” from the wide array of data available? Can you spot different types of relationships across the entities, events, and locations? Can you strengthen or weaken those connections by using your super powers to summon more data or different data? 

# Deployment

Have a MongoDB database initialized with a database YHack, and collections ActualCorporations, BannedBrokers, CourtCases, Investors. Then keep the mongod process running

Then upload the data given by FINRA for the hackathon to the database using graph.py

Then start the server using

```
python RESTapis.py
```

then access the hosted server in your browser to see the computed new bad brokers!

# Algorithm
We made a graph with nodes being all investors with edges between people working at the same company. Currently, people are marked suspicious if they are currently working at the same company as a banned broker.
We considered making use of an investor's employment history, where edges are between investors and companies they have worked at. People are marked suspicious if they have worked at a company with a history of banned brokers. We would then compute the suspicious factors by traversing the graph, assign the node a value depending on how related (determined by shortest distance in graph) an investor is with a banned broker. Unfortunately this was not implemented before submission.

# Technologies

Python, MongoDB, HTML/CSS

# Devpost 

https://devpost.com/software/suspicious-factors

