The goal of this system is to create a new system for feature requests. Many companies use ticketing systems for this but their not designed for capturing user sentiment about features they want and end up with many duplicate tickets. Users have no way of communicating how much they desire a feature, it's only done through binary upvotes/downvotes, "likes", or a bunch of +1 responses inside comments.

The goal of what users want is to provide a system where users can vote from 0-10 how much they desire a feature and limit how much they can vote per month to encourage prioritization 

Some features that will distinguish it from competitors:

User sentiment will be measured when features are requested to measure not just if someone wants something, but how much they want it.

Incentivize participation from users. Guarantee meaningful responses to features over a certain amount of votes.

Product sentiment will be measured using custom questionnaires for each user to gauge how overall satisfied they are about a product. This will allow us to figure out which features unsatisfied users request the most.

 Metrics exposed via an api so other product research, business intelligence and user feedback systems can pull this information in.

Users have limited votes they can apply to features requests in a product for a month, this incentivizes them to prioritize which features to vote for.

Desirability of a feature will be measured 1-10 instead of just a “like“ or an upvote.

Python to allow close collaboration with data scientists and psychological researchers for data analysis.

### Dev Setup

Environment variables to be set before you can run the project:
```
export FLASK_DEBUG=True # (prod should be False)
export FLASK_SECRET=insert_your_value
export DB_SALT=insert_your_value
export ADMIN_KEY=insert_your_value
```