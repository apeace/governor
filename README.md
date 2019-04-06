# Governor

A game engine and AI player for the board game Kingsburg.

**WIP**

Caveats and limitations:

 * When playing in CLI mode, the order you enter the players is the initial
   turn order. This only matters for the first King's Favor phase, when each
   player picks a free resource. Once you enter the next productive season
   you will be prompted to roll and turn order will be set. The reason initial
   turn order is set this way is because I did not feel like programming
   tie-breaking rolls. This is the only time in the game a tie-breaking roll
   is needed.

Patterns it would be interesting to look at:

 * What is the "best" first resource?
 * Does it always follow a certain building progression? Is this affected by
   what other players do?

Here are some "intelligent" behaviors it would be interesting to see:

 * Dice blocking.
 * Intentionally not building to get the King's envoy.
 * Viewing the enemy and deciding to beat it.
 * Matching soliders with players who have viewed the enemy.
