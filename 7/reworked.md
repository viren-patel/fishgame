Integration tests printed incorrecly prior to fix:
Fix:  https://github.ccs.neu.edu/CS4500-F20/hutto/commit/f154d6c07faa80d620da90ffc5f59f12293b4705

Input files for integration were formatted improperly prior to fix:
Fix: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/f154d6c07faa80d620da90ffc5f59f12293b4705

Missing Unit Tests for many functions prior to fix:
Unit Tests Added: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/5e3846592ef62db063c9aa1ef5d467182d8f6bb6

Referee was given gamestate before. Referee now makes gamestate: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/feb20998deec05d905bcc99797e396f9cb252f27

No ASCII representation of a board.  An ASCII representation was added: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/9356b8a30ea44feeb04549e4f006073f224a065d

Remove Tile Function in Board needs more description so the function was changed to remove holes given a purpose statement:https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-a2e5e9a5574dc815c4a99949d621cf78

Reachable places functionality missing in Board, this function was added to replace the old movable spaces function: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/b1f2925bed51144431c45bc1f154ff7cd98c0a6a#diff-a2e5e9a5574dc815c4a99949d621cf78

Missing data definition for game states so a purpose statement was added for the state class: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-3c0c742881289081d1c3cfb361c6da0e

Missing signature for functionality to create game states in GameState so a signature was added: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/dd86c6106c2e577e2624dfcc36586727db2c8c66#diff-3c0c742881289081d1c3cfb361c6da0e

README does not explain File and Folder Structure so the README was updated to explain File and Folder structure: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/524575b00012dafc20ed0f369f98e4ab143209c4#diff-071642fa72ba780ee90ed36350d82745

AI player only needs to send placement to referee so the AI Player was updated to do so: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/c4ca87103613db439388e901c4de59ae1484385f#diff-071642fa72ba780ee90ed36350d82745

Make separate function to handle avatar placement phase so a function was created and is now being used by run game: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/feb20998deec05d905bcc99797e396f9cb252f27#diff-071642fa72ba780ee90ed36350d82745

Referee should make initial gametree so the referee was updated to make a gametree:

Make separate function that loops over movement turns until game is over so this function was added: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/feb20998deec05d905bcc99797e396f9cb252f27#diff-071642fa72ba780ee90ed36350d82745

Referee missing abnormal conditions so the abnormal conditions were added and accounted for: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/feb20998deec05d905bcc99797e396f9cb252f27#diff-071642fa72ba780ee90ed36350d82745

No separate method/function that implements protection of calls to player so a try except added to avoid exceptions: https://github.ccs.neu.edu/CS4500-F20/hutto/commit/feb20998deec05d905bcc99797e396f9cb252f27#diff-071642fa72ba780ee90ed36350d82745
