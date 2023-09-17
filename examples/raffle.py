"""
# Raffle Participation Decision Tree

Imagine a raffle where you have different choices for how many tickets to buy
and the prices. If you estimate the total number of tickets that will be sold
and the value of the prize in dollars, you can solve for the expected value of
each ticket purchase option and make the best decision in terms of expected
monetary value.

This example breaks the problem down into small factory functions rather than
writing out each node by hand in a nested tree.
"""
from decisiontree.decisiontree import *

total_tix = 500        # Estimated total number of tickets sold
prize_value = 200.0    # My valuation of the prize

ticket_prices = {
    1.0: 1,            # $1 -> 1 ticket 
    2.0: 5,            # $2 -> 5 tickets
    3.0: 8,            # $3 -> 8 tickets
    5.0: 15,           # $5 -> 15 tickets
    10.0: 35,          # $10 -> 35 tickets
    20.0: 100          # $20 -> 100 tickets
}

def win(amt_paid):
    return Chance(
        desc="Win",
        probability= ticket_prices[amt_paid] / total_tix,
        node=OutcomeNode(value=prize_value - amt_paid),
    )

def lose(amt_paid):
    return Chance(
        desc="Lose",
        probability=1 - (ticket_prices[amt_paid] / total_tix),
        node=OutcomeNode(value=-1 * amt_paid),
    )

def ticket_decision(amt_paid):
    return Decision(
        desc=f"{ticket_prices[amt_paid]} tickets @ ${amt_paid}",
        node=ChanceNode(chances=[win(amt_paid), lose(amt_paid)])
    )

def ticket_decision_array(amounts):
    return [ticket_decision(amt) for amt in amounts]

def tree():
    prices = sorted([px for px in ticket_prices.keys()], reverse=True)
    root = DecisionNode(decisions=ticket_decision_array(prices))
    return DecisionTree(root=root)

if __name__ == "__main__":
    raffle_tree = tree()
    raffle_tree.write_jpg('raffle.jpg')
