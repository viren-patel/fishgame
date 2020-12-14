## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites:

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_
1.Todo Line 11
2. https://github.ccs.neu.edu/CS4500-F20/hutto/commit/9356b8a30ea44feeb04549e4f006073f224a065d

- a purpose statement for the "reachable tiles" functionality on the board representation
1.Todo Line 15
2.https://github.ccs.neu.edu/CS4500-F20/hutto/commit/b1f2925bed51144431c45bc1f154ff7cd98c0a6a#diff-a2e5e9a5574dc815c4a99949d621cf78

- two unit tests for the "reachable tiles" functionality
1.Todo Line 7
2.https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-0032aa430606283ef7ac98482dc6d044

### Game States


- a data definition and an interpretation for the game _state_
Todo Line 17
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-3c0c742881289081d1c3cfb361c6da0e

- a purpose statement for the "take turn" functionality on states


- two unit tests for the "take turn" functionality
1.Todo Line 7
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-5a8a51c4a0975007d74bd81a39fba2e1

### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games
This has been in place since the milestone was first handed in.
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/d623ad980e8c0117a0957b4fcd7a41698752e840#diff-a2b85550c39cc14472cf741196ccb390

- a purpose statement for the "maximin strategy" functionality on trees
This has been in place since the milestone was first handed in
https://github.ccs.neu.edu/CS4500-F20/hutto/blob/48a34403da3dd2720a38d67ce4c4472e291e9b92/Fish/Player/strategy.py

- two unit tests for the "maximin" functionality
Todo Line 7
https://github.ccs.neu.edu/CS4500-F20/hutto/blob/48a34403da3dd2720a38d67ce4c4472e291e9b92/Fish/Common/Tests/test_strategy.py

### General Issues

Point to at least two of the following three points of remediation:


- the replacement of `null` for the representation of holes with an actual representation
We have had a enum to represent tiles since the start of the project.
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/56c92755bec82c7dce45001be67f28fc1088eb14#diff-a2e5e9a5574dc815c4a99949d621cf78

- one name refactoring that replaces a misleading name with a self-explanatory name
Todo Line 13
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-a2e5e9a5574dc815c4a99949d621cf78

- a "debugging session" starting from a failed integration test:
  - the failed integration test
  - its translation into a unit test (or several unit tests)
  - its fix
  - bonus: deriving additional unit tests from the initial ones


### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).
