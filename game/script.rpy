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


# Yun's sprite image.
image yun = "images/sprites/yun.png"

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define narrator = Character(
    None,
    what_color="#ffffff",
    what_font="gui/font/Spheris-Regular.ttf"
)
define yun = Character("Yun", color="#f88787", image="yun")
define woman = Character("???", color="#d69ae2")

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

## The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene room at grayscale, opening_blur

    show expression "gui/vignette.png" as opening_vignette at heavy_vignette

    with fade

    # This plays our music file in a way that if audio captions are on,
    # it will tell us the name of the song. This music plays at full volume
    # after 2 seconds and fades out after 2 seconds when stopped.
    $ play_music(garden,fadein=2.0,fadeout=2.0)

    # This unlocks the the achievement with the corresponding name
    achieve beginning

    # These display lines of dialogue.

    narrator "Who cannot confuse the fragile outline of dream and reality?"
    narrator "The line between both, drawn by a delicate barrier of skin–a thin film that keeps the living self from dissolving into the imagined."
    narrator "The body cannot always remember which side it belongs to."
    narrator "Yun rests a fingertip on each eyelid, feeling the soft skin hugging his eyes like blankets weighing down a cold body."
    narrator "He remembers: he had closed them after tea. So how could he see her if his eyes were already shut?"
    narrator "It must’ve been another dream. As if naming it could make it harmless."
    narrator "In a way, his dreaming was a mercy. A mercy that let him exist together with her."
    narrator "For if the voice were to speak to him in the darkness he would have nothing to give but the losing."
    narrator "Someone stands just past where the light reaches."
    narrator "He doesn't try to see her clearly. Some things, in dreams, are better left at the edge."

    woman "Oh Yun, dearest Yun… What am I losing you to?"
    woman "Every night you dream so far away. I fear I might lose you to the sleeping."

    narrator "In the very same dreams she had lost Yun to, she had crossed to the other side of his days."
    narrator "No longer belonging to his waking hours, the voice begs him to stay."
    narrator "Once it was the dreams that took Yun from them. Now it was the day that did."

    woman "Don’t wake up."

# Focus on Bracelet
#
#
    woman "Can you see?"
    yun "I see too much. Even when I close my eyes."
    return