# WIP for decision tree dsl
#
#
# decision tree 1
decision:
  |> Game A
    |> chance: Outcome 1 @ 25% |> outcome: 100.0
    |> chance: Outcome 2 @ 25% |> outcome: 200.0
    |> chance: Outcome 3 @ 25% |> outcome: 300.0
    |> chance: Outcome 4 @ 25% |> outcome: 400.0
  |> Game B
    |> chance: Win @ 10% |> outcome: 12000.0
    |> chance: Lose @ 90% |> outcome: -300.0

# decision tree 2
chance:
  |> A @ 50%
    |> decision:
      |> Go
        |> chance: Win @ 90% |> outcome: 999
        |> chance: Lose @ 10% |> outcome: -1111
      |> Stay
        |> chance: Lose @ 100% |> outcome: 0
  |> B @ 50%
      |> Go
        |> chance: Win @ 90% |> outcome: 999
        |> chance: Lose @ 10% |> outcome: -1111
      |> Stay
        |> chance: Lose @ 100% |> outcome: 0
