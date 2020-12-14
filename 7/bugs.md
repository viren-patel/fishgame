Bug in state.transition found by test_run in the test_referee.py file.  The state was transitioning properly to the move of the correct player when a player ran out of moves:
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/5e3846592ef62db063c9aa1ef5d467182d8f6bb6#diff-8f14e45fceea167a5a36dedd4bea2543
Fixed by properly changing the turn index to a player with a valid move:
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/8db86aa76ecb7cb2cfcd97bdab9398dd90edecfc

Many of the prior integration tests failed due to a lack of a call to a JSON serializer before printing to stdout. The fixes are below:
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/f154d6c07faa80d620da90ffc5f59f12293b4705#diff-347934b3c3deec68d1d37e86391e0f3fR34
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/f154d6c07faa80d620da90ffc5f59f12293b4705#diff-daf969745b0a17a6e103e1f66e4999b3R58-R59
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/b9eed3e086fa69deff6e4c1f62e31a46e1570f2f#diff-4c066b68c8e8b4e8cf038db3c24f151bR47-R54
https://github.ccs.neu.edu/CS4500-F20/hutto/commit/b9eed3e086fa69deff6e4c1f62e31a46e1570f2f#diff-10c2c348e22d5d26c8688876264412a6R30-R31