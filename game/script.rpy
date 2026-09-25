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
    matrixcolor BrightnessMatrix(0.0)

transform not_talking:
    matrixcolor BrightnessMatrix(-0.3)



# images.
image yun neutral = Transform("images/sprites/yun_neutral.png", zoom = 0.85)
image yun smiling = Transform("images/sprites/yun_smiling.png", zoom = 0.85)
image yun soft = Transform("images/sprites/yun_soft.png", zoom = 0.85)
image yun closed = Transform("images/sprites/yun_closed.png", zoom = 0.85)
image yun disturbed = Transform("images/sprites/yun_disturbed.png", zoom = 0.85)
image dan neutral = Transform("images/sprites/dan_neutral.png", zoom = 0.85)
image dan serious = Transform("images/sprites/dan_serious.png", zoom = 0.85)
image dan smiling = Transform("images/sprites/dan_smiling.png", zoom = 0.85)
image nestor neutral = Transform("images/sprites/nestor_neutral.png", zoom = 0.85)
image nestor serious = Transform("images/sprites/nestor_serious.png", zoom = 0.85)
image nestor smiling = Transform("images/sprites/nestor_smiling.png", zoom = 0.85)
image location_map = "images/BG/shop.png"

init python:
    def make_speaker_focus(active_tag):
        def callback(event, interact=True, **kwargs):
            if event != "begin":
                return

            positions = {
                "yun": renpy.store.right,
                "nestor": renpy.store.left,
                "dan": renpy.store.left,
            }

            for tag, position in positions.items():
                attributes = renpy.get_attributes(tag)

                if not attributes:
                    continue

                image_name = tag + " " + " ".join(attributes)
                focus_transform = (
                    renpy.store.talking
                    if tag == active_tag
                    else renpy.store.not_talking
                )

                renpy.show(
                    image_name,
                    tag=tag,
                    at_list=[position, focus_transform],
                )

        return callback

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define narrator = Character(
    None,
    what_color="#ffffff",
    what_font="gui/font/baskervville.regular.ttf"
)
define yun = Character(
    "Yun",
    color="#faf9f9",
    image="yun",
    callback=make_speaker_focus("yun")
)
define woman = Character("???", color="#d69ae2")
define dan = Character(
    "Dan",
    color="#a2d6f9",
    image="dan",
    callback=make_speaker_focus("dan")
)
define yun_bubble = Character("Yun", image="yun", kind = bubble)
define dan_bubble = Character("Dan", image="dan", kind = bubble)
define nestor_bubble = Character("Nestor", image="nestor", kind = bubble)
define nestor = Character(
    "Nestor",
    color="#f9d6a2",
    image="nestor",
    callback=make_speaker_focus("nestor")
)

## Splashscreen

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


default pi_scene_complete = False

label shop_loop:

    call screen shop

    if _return == "PI":
        jump PI

    if _return == "mortuary":
        jump mortuary

    if _return == "wrong":
        jump wrong_location

    jump shop_loop

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
        if not pi_scene_complete:
            action Return("PI")
        else:
            action Return("wrong")

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
        if pi_scene_complete:
            action Return("mortuary")
        else:
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

    show yun neutral at right
    with dissolve

    yun '"Perhaps I brewed the tea leaves a little too well."'

    narrator "The cup is still by his elbow, colder now- a thin film has formed on the surface."
    narrator "Shelves of dried herb rise on either side of him, dust caught in the gold light swirling in the shop front. It’s quiet."
    narrator "A peaceful quiet of a pharmacy that’s been open for business for the whole time he wasn’t awake."
    narrator "He sits up too fast, making up for a shift that’s been going on without him."
    narrator "Jars. Labels. Jars. Labels. His hands work deftly, slowly."
    narrator "A porcelain beckoning cat watches from the shelf as Yun takes inventory. He dusts carefully, counts by touch as much as sight."
    narrator "The cat’s paw rises and falls in its endless loop- promise without effort. Luck, prosperity. Things given freely."
    narrator "Yun moves on. He cannot afford to wait for them."
    narrator "A bell chimes from inside the shop, a sound he associates with change. From the shared hallway, the clack of his master’s heeled shoes approach lightly."
    
    show yun neutral at right

    yun '"I wasn’t out too long, was I?"'

    show yun neutral at right
    show nestor neutral at left
    with dissolve

    nestor '"Hmm. Long enough that I served two customers while you slept through both, dear Apprentice."'

    show nestor neutral at left
    show yun neutral at right

    yun '"I’m sorry. I don’t even remember sitting down."'
    narrator "He apologizes with the humility of someone who’s had a lot of practice getting blamed. A habit he doesn’t need around his kind master."
    
    show yun neutral at right
    show nestor neutral at left
    
    nestor '"You didn’t as I recall. You were sorting jars, and then you weren’t."'

    show nestor smiling at left
    #smiling
    nestor '"Let’s try a draught that you drink outside your shift instead."'
    narrator "Yun looks down at his hands, half expecting them to be holding something still. They aren’t."
    nestor '"You look like you were dreaming awake rather than sleeping."'

    show nestor neutral at left
    show yun neutral at right

    yun '"Is there a difference anymore? With me?"'

    show yun neutral at right
    show nestor neutral at left

    nestor '"There used to be. Lately, you seem to believe less that there is."'
    narrator "Yun doesn’t answer directly. He pushes off the counter and keeps his hands busy, back to sorting jars into the shelves. The small repetitive motions standing in for what he can’t say."
    nestor '"Another dream? Do they still chase?"'

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

    show office
    with fade

    narrator "The office greets him with the faint bite of tobacco and the warmth of sandalwood. The scent clings to the lacquered furniture and the dust on the blinds."
    narrator "The window is cracked open, smoke curling out like a ghost."
    narrator "Yun doesn’t mind. The whole building breathes in herbs and ash."
    narrator "Dan sits behind his desk, sleeves rolled up, collar undone, as if he’s been arguing with the paperwork itself."
    narrator "His spine is straight from a habit no civilian job ever gave him. Even worn, his shoulders tell you who he once was."

    show dan neutral at left
    with dissolve

    dan '"Another misplaced report? Tell Nestor to keep his pharmacy from eating my papers."'

    show yun neutral at right
    with dissolve

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
    
    # Place Bleed Scene (check if keep or nah)
    dan '"Did you say something?"'
    yun '"I- Yes I did. Just now."'
    yun '"You asked who pulled the original reports."'
    dan '"I didn’t, I thought it. Don’t recall saying it out loud."'
    narrator "The silence is uncomfortable."
    yun '"...I need to sit down."'
    dan '"Yun."'
    yun '"I’m fine, it’s just- I heard you say something you didn’t say."'
    narrator "He sits. The room stays exactly as it is- smoke curling out the window, the ledger, and the files scattered on the desk."
    dan '"Say that again. Slowly this time."'
    yun '"You asked who pulled the original reports. I answered you. Then you told me you never asked it out loud."'
    dan '"Because I didn\'t"'
    yun '"I know. That\'s the part I\'m having trouble with…"'
    dan '"Kid, when’s the last time you slept? Actually slept. Not whatever it is you do on Nestor’s counter."'
    yun '"That’s not what this is."'
    narrator "Yun’s reply comes off more defensive than he’d like."
    dan'"I didn’t say it was. Answer me."'
    yun '"I..."'
    yun '"I don’t know. A while."'
    narrator "Dan exhales through his nose, it’s not quite a sigh."
    yun '"Don’t you burn the midnight oil too, Captain?"'
    narrator "Yun doesn’t miss the twitch in Dan’s eye at the title. It was a slip of the tongue."
    dan '"I’ll pretend I didn’t hear that."'
    dan '"You’ve been running on fumes and- and dream-logic for I don’t know how long."'
    dan '"And you expect me to believe you heard my thoughts and it’s not just your ears getting ahead of your sense?"'
    yun '"I know how it sounds."'
    dan '"Do you? Because it sounds to me like you’re exhausted, Yun. It sounds like too many nights arguing with something that isn’t in the room."'
    dan '"And now you’re expecting that everywhere, even outside of those nights."'
    narrator "Yun doesn’t answer right away. He thinks some of what Dan is saying might be fair."
    yun '"Maybe. I’ve thought that too. More than once, Dan."'
    dan '"But?"'
    yun '"But every time I go looking for answers there’s always something after it. Something that thinking-through can’t explain. That my exhaustion can’t be the answer."'
    narrator "Dan observes Yun carefully, and for a long moment, he gives him the same look he gave the ledger. One deciding whether this strangeness deserves investigation or dismissal."
    dan '"Alright, kid. Say I believe you heard something. Whether the building’s whispers or mine. What did I say exactly?"'
    yun '"You asked who pulled the original reports. And I told you, you did. Last spring, before the case went cold."'
    dan '"That’s true. For what it’s worth."'
    yun '"I know. I don’t know how I knew that though."'
    narrator "Dan sets his jaw, the closest he comes to looking genuinely unsettled rather than skeptical. He finds he’s been doing that more in this building."
    dan '"So either you’re pulling facts about my casework from somewhere you shouldn’t have access to, or-"'
    yun '"Or I’m just tired like you said."'
    dan '"I was going to say that I might have forgotten I even said anything. Which would be rather silly of me. A far more mundane reason that I\'d prefer."'
    #smiling
    yun '"I’d prefer that too."'
    narrator "Neither of them say anything for a while. The incense burns out and the scent of tobacco is winning again, like it always does."
    dan '"Drink some water, kid. I’m not sending you back down shaking like that. Nestor would have my head."'
    dan '"And rightly."'
    yun '"I’m alright"'
    dan '"You said that earlier, I’m not taking my chances. I didn’t believe you the first time either."'
    narrator "Yun manages something like a smile, though it doesn’t hold for long. His eyes drift towards the ledger without really meaning to."
    narrator "It’s disturbing, now that Yun’s sat down and thought about it."
    narrator "Nothing marked the moment as false as it happened. The only proof of it not being real was Dan saying so."
    narrator "And Dan could always, in principle, be lying too."
    narrator "No. He shouldn’t think that."
    narrator "Right. The woman holding a child’s bracelet."
    narrator "He dreamed of her too."

    menu:
        "Bring it up to Dan.":
            yun '"Could I ask you something? It’s unrelated…'
            dan '"You\'re already asking."'
            yun '"Has anyone reported a child’s bracelet missing recently? Jade. Cheap, intricate."'
            narrator "Dan’s face doesn’t change quickly enough to hide what it wanted to."
            dan '"Why do you ask?"'
            yun '"I don’t know. It’s just been on my mind."'
            dan '"That’s not an answer, Yun."'
            yun '"It’s the only one I have."'
            narrator "Dan doesn’t say anything for a moment too long, certainly longer than the question deserves."
            narrator "A bell chimes from somewhere in the building."
            dan '"Damn quack really doesn’t like to share employees."'
            yun '"Nestor did mention he needed me downstairs as soon as I could. Downstairs downstairs."'
            dan '"Is it urgent?"'
            yun '"He didn’t say. But I rarely get to help in the mortuary. I can’t keep him waiting."'
            dan '"Figures. The living are a second thought in this building."'
            #smiling
            yun '"Don’t be like that, Captain. I’ll be quick."'
            dan '"I’ll look into it. Go on, Nestor’s waiting on you."'
            dan '"Unless you’d rather sit here with me worrying about jewelry, which I prefer you not. Your master will have a great say in my always hogging your time."'
            yun '"I’ll take the excuse to leave actually."'
            dan '"Smart man."'
        
        "Ask about going downstairs.":
            narrator "A bell chimes from somewhere in the building."
            yun '"Nestor needs me downstairs. I should go."'
            dan '"Running from me or the conversation?"'
            yun '"Can’t it be both?"'
            dan '"Fair enough. Go on, then."'
            narrator "Yun leaves the thought unsaid. Whatever the thought was stays exactly as it is."
            yun '"Thank you, Dan."'
            dan '"Light some incense before coming back. Don’t go bringing his business into mine."'
    $ pi_scene_complete = True
    jump shop_loop

######################################################
# Scene 4
######################################################

label mortuary:
    narrator "These stairs don’t end where he remembers. He counts them anyway, an old habit out of an old order."
    narrator "Beneath him the temperature changes before the stairwell does. Cold air comes up to greet him. It always does on the way to the mortuary."
    narrator "But today it arrived soon"
    narrator "Yun stares into the void. The stairs seem longer by the second."
    narrator "A bracelet catches light before he sees who’s holding it."
    woman '"You’re going the wrong way."'
    yun '"I’m going the way I always go."'
    woman '"Not today."'
    narrator "His hands reach out for the railing, and it isn’t there. Not gone, just farther away than his hand expected."
    woman '"Don’t wake up."'
    yun '"I’m not asleep."'
    woman '"Then why are you counting?"'
    narrator "He looks down at his feet and can’t remember what step he’s on. The dark beneath him doesn’t answer either."
    
    # Put CG
    yun '"Vertigo."'
    yun '"It is not the fear of falling, but the desire to. The pull…downward, to the depths."'
    yun '"A sweet resounding summons to renounce my waking self. In moments of weakness, I found I was ready to heed the call– to descend to a place where no one ever wakes."'
    narrator "There is no mortuary at the bottom. Only more stairs."
    narrator "Then his shoulder hits a doorframe. Nestor’s voice is already mid-sentence, as if no time passed at all."

    nestor '"-there you are. I’ll need your hands today."'
    narrator "Yun nods."
    yun '"Of course."'
    narrator "Nestor gestures toward the table, to the covered form beneath the sheet."
    nestor '"Nothing complicated. Just help me bring him up, keep things steady. If you feel yourself drifting, say so. We can slow down."'
    narrator "Yun draws a quiet breath."
    yun '"Alright."'
    narrator "Nestor turns back to the table, already reaching for the cloth. Yun stands behind Nestor, blocking the draft from the staircase."
    narrator "His posture is stiff, arms locked at parade rest. An old habit his body always reaches for."
    narrator "Nestor opens a tin of balm, the metal sliding softly in his hands."
    nestor '"Follow my movement. We go together."'
    narrator "Yun doesn’t notice he’s holding his breath."
    nestor '"At ease."'
    yun '"Right..."'
    nestor '"The wind moves freely. You can too, Yun. Don’t hold yourself hostage to stillness."'
    narrator "The body waits. So do they."
    narrator "Yun steps closer, the floor cold under his shoes. Fingers hover over the sheet, hesitant. And the strange urge to apologize is swallowed before it becomes a word."
    narrator "The weight…of a person in death. The same weight he carries from his dreams."
    narrator "He sees himself in the cadaver. He shouldn’t."
    narrator "Still, he wonders if he too is weightless-yet burdened- when he is not awake."
    yun '"Should I lift it…like this?"'
    nestor '"Carry the weight with your arms, Yun. Not your mind. Feel it, don’t think it."'
    yun '"Like this."'
    nestor '"Better."'
    narrator "Nestor works beneath and around what Yun holds steady, completely trusting Yun to lift."
    nestor '"You are stronger than you look, dear Apprentice."'
    yun '"It’s heavier than I expected. Nothing I can’t carry. Just…strange."'
    nestor '"Burdens do not weigh the body post mortem. Still, it is not light–the weight of death."'
    narrator "Yun’s eyes briefly catch the tin beside them. For a moment it isn’t his reflection he half-sees there."
    narrator "A man in uniform. A version of himself he has tried to no longer answer to."
    narrator "He blinks, and it’s Yun again."
    yun '"He looks…young."'
    nestor '"He is."'
    yun '"That doesn’t feel right."'
    nestor '"No. But such is the way of things. It was his life to finish."'
    yun '"Sometimes I think… if I’d done more. If I were faster. Better. Maybe some of them wouldn’t be down here."'
    nestor '"You are very fond of bargaining with time."'
    yun '"I don’t like wasting it."'
    yun '"My existence, I can justify it… Not for any reason like my right to live. But because I’m needed. I have to be."'
    nestor '"You say that like it isn’t enough that you are here."'
    yun '"Is it?"'
    nestor '"An old argument. You’ve had it with yourself longer than with me."'
    narrator "Nestor wipes his hands on a cloth, allowing Yun to think in the pause."
    nestor '"I suggest you learn from your mistakes. Suffer less for them. Doctor’s advice."'
    #smiling
    yun '"You’re not a doctor."'
    #smiling
    nestor '"My clients would say I am. In a way."'
    narrator "The last of it is quiet work. Yun wipes the table in exact, measured strokes. Straight lines. No overlap. No waste."
    narrator "Too careful."
    narrator "His hand slows, then stops altogether."
    narrator "He notices it- how rigid his wrist has become, how his breath has gone shallow."
    narrator "He deliberately smears the cloth in a wider arc. Messier. Human. The surface is still clean. His shoulders loosen."
    nestor '"You did well."'
    yun '"What?"'
    nestor '"I've seen you do that correction over the years. Tight, then loose, and now honest."'


    return
