# The script of the game goes in this file.

transform grayscale:
    matrixcolor SaturationMatrix(0.0)

transform opening_blur:
    blur 12.0

transform heavy_vignette:
    xsize 1280
    ysize 720
    align (0.5, 0.5)
    alpha 0.85

transform talking:
    ease 0.15 zoom 1.0
    matrixcolor BrightnessMatrix(0.0)

transform not_talking:
    ease 0.15 zoom 0.95
    matrixcolor BrightnessMatrix(-0.3)



# images.
image yun neutral = "images/sprites/yun_neutral.png"
image yun smiling = "images/sprites/yun_smiling.png"
image yun soft = "images/sprites/yun_soft.png"
image yun closed = "images/sprites/yun_closed.png"
image yun disturbed = "images/sprites/yun_disturbed.png"
image dan neutral = "images/sprites/dan_neutral.png"
image dan serious = "images/sprites/dan_serious.png"
image dan smiling = "images/sprites/dan_smiling.png"
image nestor neutral = "images/sprites/nestor_neutral.png"
image nestor serious = "images/sprites/nestor_serious.png"
image nestor smiling = "images/sprites/nestor_smiling.png"
image location_map = "images/BG/shop.png"

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define narrator = Character(
    None,
    what_color="#ffffff",
    what_font="gui/font/baskervville.regular.ttf"
)
define yun = Character("Yun", color="#faf9f9", image="yun")
define woman = Character("???", color="#d69ae2")
define dan = Character("Dan", color="#a2d6f9", image="dan")
define yun_bubble = Character("Yun", image="yun", kind = bubble)
define dan_bubble = Character("Dan", image="dan", kind = bubble)
define nestor_bubble = Character("Nestor", image="nestor", kind = bubble)
define nestor = Character("Nestor", color="#f9d6a2", image="nestor")

## Splashscreen ############################################################
## A portion of the game that plays at launch, before the main menu is shown.
## https://www.renpy.org/doc/html/splashscreen_presplash.html

## The animation is boring so I recommend using something else.
## ATL documentation: https://www.renpy.org/doc/html/atl.html

image splash_anim_1:

    "gui/renpy-logo.png"
    xalign 0.5 yalign 0.5 alpha 0.0
    ease_quad 7.0 alpha 1.0 zoom 2.0

default persistent.firstlaunch = False

label splashscreen:
    
    scene black

    ## Here begins our splashscreen animation.
    show splash_anim_1
    show text "{size=60}Made with Ren'Py [renpy.version_only]{/s}":
        xalign 0.5 yalign 0.8 alpha 0.0
        pause 6.0
        linear 1.0 alpha 1.0
    
    ## The first time the game is launched, players cannot skip the animation.
    if not persistent.seen_splash:
        
        ## No input will be detected for the set time stated.
        ## Set this to be a little longer than how long the animation takes.
        $ renpy.pause(8.5, hard=True)
 
        $ persistent.seen_splash = True
    
    ## Players can skip the animation in subsequent launches of the game.
    else:
 
        if renpy.pause(8.5):
 
            jump skip_splash

    scene black
    with fade
 
    label skip_splash:
 
        pass
    
    call screen content_warning

    ## The first time the game is launched, players can set their accessibility settings.
    if not persistent.firstlaunch:

        call screen splash_settings

        call screen preferences

        ## This screen will not appear in subsequent launches of the game when
        ## the following variable becomes true.
        $ persistent.firstlaunch = True

    return

label shop_loop:

    call screen shop

    if _return == "wrong":
        jump wrong_location

    if _return == "PI":
        jump PI

screen shop():

    add "images/BG/shop.png"

    # Left door
    imagebutton:
        idle Solid("#00000000")
        hover Solid("#ffffff22")
        xpos 45
        ypos 80
        xsize 340
        ysize 510
        action Jump("PI")

    # Middle door
    imagebutton:
        idle Solid("#00000000")
        hover Solid("#ffffff22")
        xpos 515
        ypos 75
        xsize 305
        ysize 520
        action Return("wrong")

    # Right door
    imagebutton:
        idle Solid("#00000000")
        hover Solid("#ffffff22")
        xpos 975
        ypos 45
        xsize 265
        ysize 560
        action Return("wrong")

label wrong_location:

    scene black
    yun '"Need to get these to Dan first."'
    jump shop_loop




## The game starts here.

label start:

    scene room at grayscale, opening_blur
    play music dream fadein 1.0 fadeout 1.0 loop

    show expression "gui/vignette.png" as opening_vignette at heavy_vignette

    with fade


    narrator "Who cannot confuse the fragile outline of dream and reality?"
    narrator "The line between both, drawn by a delicate barrier of skin–a thin film that keeps the living self from dissolving into the imagined."
    narrator "The body cannot always remember which side it belongs to."
###############################################################################################################
    # Both grey initially.
    #show yun at sprite_gray(0, 0.0)
    #show dan at sprite_gray(1200, 1.0)

    # Yun speaks.
    #show yun at sprite_position(0, 0.0)
    #yun_bubble "Hi"

    # Dan speaks.
    #show yun at sprite_gray(0, 0.0)
    #show dan at sprite_position(1200, 1.0)
    #dan_bubble "Hello"

    # Both grey afterward.
    #show yun at sprite_gray(0, 0.0)
    #show dan at sprite_gray(1200, 1.0)
############################################################################################################
    narrator "Yun rests a fingertip on each eyelid, feeling the soft skin hugging his eyes like blankets weighing down a cold body."
    narrator "He remembers: he had closed them after tea. So how could he see her if his eyes were already shut?"
    narrator "It must’ve been another dream. As if naming it could make it harmless."
    narrator "In a way, his dreaming was a mercy. A mercy that let him exist together with her."
    narrator "For if the voice were to speak to him in the darkness he would have nothing to give but the losing."
    narrator "Someone stands just past where the light reaches."
    narrator "He doesn't try to see her clearly. Some things, in dreams, are better left at the edge."

    scene room at grayscale

    show expression "gui/vignette.png" as opening_vignette at heavy_vignette

    woman '"Oh Yun, dearest Yun… What am I losing you to?"'
    woman '"Every night you dream so far away. I fear I might lose you to the sleeping."'

    narrator "In the very same dreams she had lost Yun to, she had crossed to the other side of his days."
    narrator "No longer belonging to his waking hours, the voice begs him to stay."
    narrator "Once it was the dreams that took Yun from them. Now it was the day that did."

    woman '"Don’t wake up."'

# Focus on Bracelet
# (Zoom in on bracelet)
#
    woman '"Can you see?"'
    yun '"I see too much. Even when I close my eyes."'

    scene black with fade

#######################
# Scene 2
#######################

    scene black

    yun '"I...see too much..."'
    narrator "Yun’s fingers caress his eyelids, the touch telling him his eyes were still closed. He opens them to soft afternoon light."

    stop music fadeout 1.0

    scene room with Fade(0.5, 0.5, 1.0)
    play music pharmacy fadein 1.0 fadeout 1.0 loop

    narrator "It is the sheep hour. He wondered when he had fallen asleep."

    show yun neutral at right, talking
    with dissolve

    yun_bubble '"Perhaps I brewed the tea leaves a little too well."'

    narrator "The cup is still by his elbow, colder now- a thin film has formed on the surface."
    narrator "Shelves of dried herb rise on either side of him, dust caught in the gold light swirling in the shop front. It’s quiet."
    narrator "A peaceful quiet of a pharmacy that’s been open for business for the whole time he wasn’t awake."
    narrator "He sits up too fast, making up for a shift that’s been going on without him."
    narrator "Jars. Labels. Jars. Labels. His hands work deftly, slowly."
    narrator "A porcelain beckoning cat watches from the shelf as Yun takes inventory. He dusts carefully, counts by touch as much as sight."
    narrator "The cat’s paw rises and falls in its endless loop- promise without effort. Luck, prosperity. Things given freely."
    narrator "Yun moves on. He cannot afford to wait for them."
    narrator "A bell chimes from inside the shop, a sound he associates with change. From the shared hallway, the clack of his master’s heeled shoes approach lightly."
    
    show yun neutral at right, talking

    yun_bubble '"I wasn’t out too long, was I?"'

    show yun neutral at right, not_talking
    show nestor neutral at left, talking
    with dissolve

    nestor_bubble '"Hmm. Long enough that I served two customers while you slept through both, dear Apprentice."'

    show nestor neutral at left, not_talking
    show yun neutral at right, talking

    yun_bubble '"I’m sorry. I don’t even remember sitting down."'
    narrator "He apologizes with the humility of someone who’s had a lot of practice getting blamed. A habit he doesn’t need around his kind master."
    
    show yun neutral at right, not_talking
    show nestor neutral at left, talking
    
    nestor_bubble '"You didn’t as I recall. You were sorting jars, and then you weren’t."'

    show nestor smiling at left, talking
    #smiling
    nestor_bubble '"Let’s try a draught that you drink outside your shift instead."'
    narrator "Yun looks down at his hands, half expecting them to be holding something still. They aren’t."
    nestor_bubble '"You look like you were dreaming awake rather than sleeping."'

    show nestor neutral at left, not_talking
    show yun neutral at right, talking

    yun_bubble '"Is there a difference anymore? With me?"'

    show yun neutral at right, not_talking
    show nestor neutral at left, talking

    nestor_bubble '"There used to be. Lately, you seem to believe less that there is."'
    narrator "Yun doesn’t answer directly. He pushes off the counter and keeps his hands busy, back to sorting jars into the shelves. The small repetitive motions standing in for what he can’t say."
    nestor_bubble '"Another dream? Do they still chase?"'

    menu:
        '"They do."':
            yun '"They do. I just stopped running from them."'
            narrator "Yun nervously fiddles with the mortar, half-expecting disappointment from the master."
            narrator "Nestor is busy writing on paper."
            nestor '"There’s balance in that too. We must dream and wake in turn. Do not lose your waking hours running."'
            narrator "Somehow, coming from him, that’s enough for Yun. Nestor's voice carries like incense smoke– soft and sure. It grounds him in the afternoon light."
        
        "Stay Quiet.":
            yun '"..."'
            yun '"I just need to wake up properly."'
            
    narrator "He brushes past Nestor, straightening jars, warming away the cold pull of sleep on his body."
    nestor '"Waking yourself has become quite the habit. Try not to harm yourself doing it."'
    nestor '"The whole body shares the pain of even the little finger."'
    yun '"I’m getting better at telling when I’m still dreaming."'
    nestor '"Hm. Then keep your hands busy. Often it is the body that knows what’s real before the mind."'
    yun '"That’s what you’re here for."'
    narrator "Nestor smiles, not a rare sight, but always comforting."
    nestor '"You’ll be alright, Yun."'
    narrator "Nestor turns his attention to work before Yun can answer, as if the matter’s settled itself. Yun does the same, deciding to believe in his words the way he always does."
    yun '"So many prescriptions… Has everyone in this district fallen ill?"'
    nestor '"Good for business, I say."'

    # nestor smiling
    nestor '"And good for keeping your hands busy."'
    yun '"Alright. Back to work. Just match the herbs into the packet the list calls for, like usual."'

    # minigame start
    call screen herb_minigame

    if _return:

        if herb_mislabeled_clue_found:
            narrator "There’s a name crossed out messily in ink. Not a habit either of them have."
            yun '"Hm? Was this crossed out on purpose?"'
            yun '"I should check the ledger."'
            narrator "Yun finds the ledger exactly where he remembers leaving it. He flips to a list of customers, fingers running through all the names."
            yun '"There. Nyima..."'
        else:
            yun '"Done and dusted. I should update the inventory."'
            narrator "Yun finds the ledger exactly where he remembers leaving it, still open and waiting for ink."

    # minigame end
    yun '"That\'s strange..."'
    narrator "The page he filled out before closing is gone, replaced by new entries written in a hand immediately recognized. Dan’s, his other boss on the floor above."

    menu:
        "Read the pages further.":
            narrator "Yun flips back, page by page, trying to discern whose handwriting was whose."
            narrator "Where does it end? Where does Dan’s or his begin?"
            yun '{i}quietly{/i}  "There’s more than I thought."'
            yun '"Did he stay all night writing after me?"'
            narrator "His quiet words reach Nestor still, who straightens his back and offers Yun a smile."
        
        "Ask Nestor about the writing":
            yun '"That\'s odd..."'
            yun '"Did Dan update this?"'
        
    nestor '"You’ll have to ask him. Our ledgers have grown fond of each other lately."'
    yun '"It must\'ve been mixed up. I’ll take it to him."'
    nestor '"While you’re at it, do tell him to keep his paperwork off my counter next time."'
    nestor '"The living and the dead already share too many spaces."'
    narrator "Nestor doesn’t read the ledger. He closes it and hands it to Yun’s firm grasp. If he was uneasy, Yun couldn’t tell."
    narrator "Nestor always liked to keep the pharmacy tidy, the clutter predictable."
    narrator "But lately, things seem to move when no one’s looking."
    narrator "Yun turns toward the stairwell. As he passes, the cat continues its motion- patient, unblinking. It will still be there when he returns. It always is."

    jump shop_loop


#########################################
# Scene 3
#########################################

label PI:

    scene black
    with fade

    narrator "The stairs to the PI office share a landing with the stairs that lead down the mortuary. The building’s never cared to separate the living from what awaits."
    narrator "Yun walks to meet the stairwell, feeling the cool chill coming from the mortuary’s stairs, then up to the second floor."
    narrator "The air is somehow always warmer around the door to Dan’s office."
    narrator "Yun glances at the documents in his hand. The ink is fresh, as if re-written. He remembers placing these in Dan’s desk. Or did he dream that too?"
    narrator "{b}(Knocks){/b}"
    dan '"If that’s you, Yun, the door’s open. Unless you’re here to peddle, then it’s locked."'
    yun '"There’s been a mix-up. You left your reports in the pharmacy."'
    narrator "Yun turns the knob and eases the door open; it creaks with a groan."
    narrator "The office greets him with the faint bite of tobacco and the warmth of sandalwood. The scent clings to the lacquered furniture and the dust on the blinds."
    narrator "The window is cracked open, smoke curling out like a ghost."
    narrator "Yun doesn’t mind. The whole building breathes in herbs and ash."
    narrator "Dan sits behind his desk, sleeves rolled up, collar undone, as if he’s been arguing with the paperwork itself."
    narrator "His spine is straight from a habit no civilian job ever gave him. Even worn, his shoulders tell you who he once was."
    dan '"Another misplaced report? Tell Nestor to keep his pharmacy from eating my papers."'
    yun '"He thinks yours wandered over first."'
    narrator "Yun places the documents on the desk, careful not to disturb the others."
    yun '"I thought I left these here last night."'
    narrator "Dan glances at the pages, then at Yun. The man looks like he hasn’t slept either, though his sleeplessness seems earned."
    narrator "Work, not worry."
    narrator "Yun’s isn’t so easy to name."
    dan '"No one should be shuffling between my office and the pharmacy."'

    menu:
        '"No one but me."':
            dan '"Sleepwalking, then? You ought to have Nestor fix a draught. One that keeps you awake this time."'
            yun '"I’ll ask him to make one strong enough for both of us."'
            narrator "The air lightens, the tension within Yun somewhat eased as he gives a smile."
            dan '"Let’s all try not to sort files half-asleep–your master included."'

        "Yun doesn’t answer, instead tracing the edges of the paper with his thumb.":
            dan '"If your silence is suggesting Nestor’s clients are moving our reports, don’t."'
            narrator "Dan leans back, the floor creaking under his weight."
            dan '"Not every strange thing that happens in this place needs a ghost behind it."'
            narrator "He says it firmly, but Yun wonders if he’s convincing himself more than anyone else."
            dan '"If Nestor isn’t worried, you shouldn’t be either. You trust him, don’t you?"'
        
        '"You think someone’s been…moving things around?"':
            narrator "Dan looks up, studying his face for longer than he should."
            dan '"You worry too much, kid. Papers move, people forget. That’s all."'
            narrator "Dan leans back in his chair, the floor creaking beneath him."
            dan '"This building’s old. Things shift, settle. Doesn’t mean it’s out to haunt you."'
    
    narrator "Yun nods, his hands reach for the stack of documents on the table, even as his attention shifts. He sorts through the files- and then he finds it."

    if herb_mislabeled_clue_found:
        
        narrator "A name, the very same crossed out name he found earlier. A coincidence too specific to be nothing, yet too small to be anything."
        yun '"This name… It’s the same one as the prescription downstairs."'
        narrator "Dan takes the file from him, unhurried, but to Yun it feels deliberate."
        dan '"Same how?"'
        yun '"I don’t know yet. But it’s the same name as Nestor’s list."'
        narrator "Dan puts out his cigar in the ashtray, taking his time with his reply. He sets the file down, not quite dismissing it, not quite approving either."
        narrator "Yun recognizes this habit. When Dan decides how much truth a room can handle."
        dan '"Leave it with me, Yun."'
        yun '"That’s not a no."'
        dan '"It’s not a yes, either. Leave it with me."'
        narrator "Yun doesn’t budge."
        dan '"Didn’t your Master tell you not to chase too many mysteries?"'
        yun '"This is an investigation firm."'
        dan '"Hm. That it is."'
        narrator "He pulls the file back to himself, opening it properly and deciding it is worth reading after all. Even if he won’t say it out loud."
        narrator "Yun parses through more files, arranging them."
        dan '"Who pulled the original reports on this?"'
        yun '"You did, last spring. Before the case went cold."'
        narrator "Dan’s pen stops."
    
    else:
        narrator "As if it floats above the rest of the text, a name. It's awfully familiar to Yun. He’s never known this person but it feels important."
        yun '"This name… I feel like I know it."'
        yun '"It sounds strange, but I feel I’m missing too much, like sand falling through my fingers for not knowing. It stands out so much, but why?"'
        dan '"Like I said, you worry too much. Leave that old case to me."'
        narrator "Dan takes a long drag of his cigar, carefully breathing the smoke out the window and away from Yun."
        narrator "Yun recognizes he’s deep in thought. Not quite dismissing his concern, not quite approving either."
        narrator "Dan goes back to his own paperwork, leaving the case file on the corner of his desk. Its name unsaid, whatever it meant exactly where Yun left it."
        narrator "The scritch of the detective’s ink fills the silence. Yun parses through more files, arranging them."
        dan '"Who pulled the original reports on the Cao business anyway? Not me."'
        yun '"You did, last spring. Before the case went cold."'
        narrator "Dan’s pen stops."
    








    return
