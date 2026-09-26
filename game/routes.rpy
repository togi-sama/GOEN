## Ending route and flag logic for GOEN.
##
## Two axes are tracked across the run:
##
##   route_acknowledge - Yun admits, engages with, or asks for help about the
##                        dreams. He stops carrying them alone.
##   route_pursue      - Yun chases the case: the crossed-out name, the
##                        bracelet, the things moving on their own.
##
## Placing flags: drop a single call into the menu branch you want to count.
##
##     menu:
##         "Read the pages further.":
##             $ pursue()
##             ...
##
##         "Ask Nestor about the writing.":
##             $ acknowledge()
##             ...
##
## Options you deliberately leave with no call are the deflecting ones. They
## cost the player the ending, which is the point.
##
## TIMING: pursue() is gated behind herb_mislabeled_clue_found, and that clue
## only becomes available from the herb minigame partway through `start`. Any
## menu placed before the minigame therefore cannot grant Pursue at all. As of
## writing the menus in order are:
##
##     start  - "They do." / "Stay Quiet."                (BEFORE the clue)
##     start  - "Read the pages further." / "Ask Nestor."  (after)
##     PI     - three-way, Dan on the shuffling reports   (after)
##     PI     - the child's bracelet                       (after)
##     mortuary - "Tell Nestor about the dream." / "Say Nothing."  (after)
##
## So Pursue's three points must come from three of the four post-clue menus,
## and Acknowledge's from the pre-clue menu plus two others.


#############################################################
## Route state
#############################################################

default route_acknowledge = 0
default route_pursue = 0

## Set by the dispatcher to "a", "b", or "c". Useful for achievements,
## save-file inspection, and branching dialogue inside an ending.
default route_ending = None

## Endings the player has reached across all playthroughs. Stored as a set;
## see unlock_ending() for why it is reassigned rather than mutated.
default persistent.endings_seen = set()

## Unlocks the Developer Notes slot in the Extras menu.
default persistent.game_clear = False

default persistent.credits_seen = False

## Where a player lands when no ending condition matches. A bare 2 on one axis
## with 0 on the other satisfies none of the three conditions below, so this
## catches it. Change to "d" (and add an ending_d label) if that case should
## get its own ending.
define ROUTE_FALLBACK = "c"

## The ending the player is currently working toward. Kept separate from
## ENDING_LIST so the dispatcher has a single source of truth for the rules.
define ROUTE_THRESHOLD = 2


#############################################################
## Ending table
#############################################################

## (id, revealed title, blurb). The title and blurb are only shown once the
## player has actually reached that ending; until then the gallery shows ???.
## Titles and blurbs are placeholders -- rename them to fit the final prose.

define ENDING_LIST = (
    ("a", _("Held to the Light"), _("placeholder blurb")),
    ("b", _("Laid to Rest"), _("placeholder blurb")),
    ("c", _("Unresolved"), _("placeholder blurb")),
)


#############################################################
## Point helpers -- these are the flag-placement API
#############################################################

init python:

    def acknowledge(amount=1):
        """Add to the Acknowledge axis. Always permitted."""
        global route_acknowledge
        route_acknowledge += amount
        return route_acknowledge

    def pursue(amount=1):
        """Add to the Pursue axis, but only once the mislabeled clue is found.

        This is what makes it impossible to reach more than ROUTE_THRESHOLD
        Pursue without the clue: without it, this grants nothing. Returns the
        points actually granted, so 0 means the clue had not been found yet.
        """
        global route_pursue

        if not herb_mislabeled_clue_found:
            return 0

        route_pursue += amount
        return route_pursue

    def route_lead():
        """Which axis the player is currently further along, or None if tied.

        Only used for flavour text and the ending gallery subtitle -- the
        ending itself is decided by resolve_route(), never by this.
        """
        if route_acknowledge > route_pursue:
            return "acknowledge"
        if route_pursue > route_acknowledge:
            return "pursue"
        return None

    def route_summary():
        return "acknowledge %d / pursue %d" % (route_acknowledge, route_pursue)


#############################################################
## Ending resolution
#############################################################

init python:

    def resolve_route():
        """Work out which ending the player has earned.

        Ending A  Pursue is dominant, and the mislabeled clue was found.
        Ending B  Acknowledge is dominant.
        Ending C  Yun gave ground on both axes, neither exceeding one point.

        The three conditions are mutually exclusive: A needs Pursue above
        ROUTE_THRESHOLD, B needs Acknowledge above it, and C requires both
        axes to be at or below one. So no tie-breaking order is required.

        Returns "a", "b", or "c".
        """
        if route_pursue > ROUTE_THRESHOLD:
            return "a"

        if route_acknowledge > ROUTE_THRESHOLD:
            return "b"

        if route_acknowledge <= 1 and route_pursue <= 1:
            return "c"

        ## A bare 2 on one axis with 0 on the other matches nothing above.
        return ROUTE_FALLBACK

    def unlock_ending(eid):
        """Record an ending as reached and unlock the post-game extras.

        The set is reassigned rather than mutated in place on purpose:
        Ren'Py's Persistent only flags itself as changed when the attribute
        is assigned, so persistent.endings_seen.add(eid) would never save.
        """
        if eid not in persistent.endings_seen:
            persistent.endings_seen = persistent.endings_seen | set([eid])

        persistent.game_clear = True

        renpy.save_persistent()

    def ending_seen(eid):
        return eid in persistent.endings_seen

    def ending_progress_text():
        return _("Endings reached: %d of %d") % (
            len(persistent.endings_seen),
            len(ENDING_LIST),
        )


#############################################################
## Endings
#############################################################

## Shared setup for the three endings, per the hybrid structure: everything
## repetitive lives here so the prose below each ending can be written out in
## full without inherited scaffolding getting in the way.
label ending_prologue(ending_id):

    scene black with fade
    stop music fadeout 1.0

    ## Granting through the python entry point rather than the `achieve`
    ## statement, because the id is a parameter here.
    $ bobcachievement_grant(ending_id)

    ## Idempotent, and also covers a player who arrives here via Replay or a
    ## loaded save rather than through the dispatcher.
    $ unlock_ending(ending_id)

    return


## Ending A -- Pursue dominant, mislabeled clue found.
label ending_a:

    call ending_prologue("a")

    narrator "By the time he’s home, the day’s hold on him doesn’t slip."
    narrator "He doesn’t remember lying down. He rarely does anymore. The barrier between going to sleep and waiting for it to arrive has thinned that he can no longer notice when he crosses."
    nestor '"Yun"'
    narrator "It’s morning, at least he thinks it is. Yun’s back at the counter. What hour is it anyway? Ox? Rabbit? It doesn’t matter anymore. He works as he always does."
    nestor '"Yun."'
    yun '"I heard you the first time."'
    nestor '"There wasn’t a first time."'
    narrator "Nestor’s voice carries a hint of worry, a fear that has witnessed this exact failure. He’d hoped never to watch it twice."
    narrator "Yun’s hands are steady. His eyes though, are somewhere Nestor can’t follow him to."
    narrator "He chased the thread until he caught it. He wasn’t taught what to do when it caught him back."


    return


## Ending B -- Acknowledge dominant.
label ending_b:

    call ending_prologue("b")

    narrator "Yun doesn’t remember sleeping. It’s still light outside, he’s back at the counter."
    narrator "The day’s exhaustion must have caught up with him. Hours of navigating his dreams carefully was starting to show."
    narrator "Dan comes to mind. His skepticism but mostly his care. He looks up the stairwell where Dan should be. And then he looks at Nestor."
    narrator "Yun stares at Nestor’s back, his reliable master. His words from downstairs seem to wash him ashore. He’ll be okay."
    narrator "Neither have left. They were in the building with him, even as he slept."
    narrator "He pauses. Two fingers rise, pressing briefly against his eyelids. Warm skin. Closed after tea. He opens his eyes."
    narrator "The pharmacy is still there. The jars haven’t moved. The light hasn’t shifted."
    narrator "He lowers his hand and exhales."
    yun '"I’m here."'
    narrator "He says not to convince himself, but because it’s true."
    narrator "Behind the counter, seeing him wake, Nestor turns back to his work. The day continues."
    narrator "And Yun stays awake."


    return


## Ending C -- both axes held at or below one point. Also catches the
## ROUTE_FALLBACK case, so this is where every unclassified run lands.
label ending_c:

    call ending_prologue("c")

    narrator "By the time he’s home, the day’s hold on him slowly starts to slip. There’s no thinking back on it. He closes his eyes."
    narrator "He doesn’t remember lying down. And there’s nothing strange in that, most nights go the same way and this doesn’t ask to be different."
    woman '"You didn’t look today."'
    yun '"There wasn’t anything to look at."'
    woman '"There shouldn’t be. Until there is."'
    narrator "The voice drowns out. Yun will forget what was said come morning. Not a fault of memory, it’s just how an ordinary day costs him, nothing- and gives him, also nothing."
    narrator "He’ll wake and the pharmacy will be there unchanged, exactly as he left it. His hands will reach for the first jar and work will begin."
    narrator "Another ordinary day. He really was just tired."

    return
