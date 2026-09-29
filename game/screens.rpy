################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    unscrollable "hide"

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

## We need to redefine the `centered` speaker so the textbox doesn't appear due
## to the custom opacity slider.

screen cinematic_bars():

    $ bar_height = 40

    add Solid("#000000"):
        xsize config.screen_width
        ysize bar_height
        xpos 0
        ypos 0

    add Solid("#000000"):
        xsize config.screen_width
        ysize bar_height
        xpos 0
        yalign 1.0


define centered = Character(None, window_background=None)

screen say(who, what):
    style_prefix "say"

    ## The quick menu is an overlay screen (see options.rpy), so this flag is
    ## what shows/hides its tab. Set here so it reappears once a say-menu or
    ## choice screen is dismissed.
    $ quick_menu = True

    window:

        add Transform("gui/green.png", yzoom=0.4, yoffset=-140, alpha = 1.0)

        ## The window background is held by this Transform rather than by the
        ## window's own style, so its alpha is set here.

        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    ### Or, just comment out the if not and shift the side image back one tab
    ### if the side image is important to your GUI
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height


style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    font "gui/font/baskervville.regular.ttf"
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    font "gui/font/baskervville.regular.ttf"
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False
    line_spacing gui.preference("dialogue_spacing", 2)

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    ## Hide the quick menu tab while choices are on screen, so it can't sit on
    ## top of the options. screen say sets this back to True afterwards.
    $ quick_menu = False

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

## The quick menu is a tab at the top right that expands into a vertical panel
## of buttons. Both are painted art from gui/button/menu. The panel art also
## bakes in a second side-button tab at its top-left, which is what collapses
## the panel again (see the hotspot in quick_menu_panel).
##
## Asset geometry (measured from the alpha masks, both are white art so they're
## invisible against a white background):
##
##   side button.png  -- 81x121 canvas, art at x 37..80, y 12..114 (44x103).
##                       A rounded tab with three horizontal lines, flush
##                       against the canvas's RIGHT edge.
##   quick_menu.png   -- shipped as a full 1280x720 canvas. The panel body is
##                       at x 1084..1279, y 99..490 (196x392) with a second
##                       side-button tab protruding to its left at
##                       x 1039..1086, y 106..212. The panel screens crop it
##                       (see quick_menu_panel) to a 273x436 canvas: 32px of
##                       left padding, then the tab, then the body. In crop-
##                       local coordinates the body spans x 77..272, y 19..410,
##                       and the tab x 32..79, y 26..132.
##
## side button.png is added uncropped at xalign 1.0 and its left padding hangs
## off-screen; quick_menu.png is cropped first and then right-aligned. When
## right-aligned, quick_menu.png's art covers screen x 1039..1280, and side
## button.png's art covers screen x 1236..1280.
##
## How the animation works
## -----------------------
## Ren'Py 8.5's ATL has no "if" statement, so a transform can't react to
## quick_menu_open on its own. The panel is therefore a separate screen that
## QuickMenuToggle shows and hides imperatively, and the slide lives in its
## "on show"/"on hide" hooks -- the same mechanism screen notify uses for its
## fade out. Ren'Py keeps the screen alive until the on-hide animation
## finishes, which is what lets the panel slide away instead of blinking out.
##
## The closed tab (top right) lives in the overlay screen below and simply
## isn't drawn while the panel is open, so it vanishes the instant the panel
## opens rather than sliding along with it. Closing brings it straight back.
## Collapsing is handled instead by an invisible hotspot over the tab baked
## into the panel art's own top-left corner (see quick_menu_panel).
##
## The panel screen is shown/hidden imperatively by QuickMenuToggle rather than
## with "use", because a "use"d child can't carry an on-show animation.
##
## The hover lean works differently, because it must move the button's hitbox as
## well as its art (see quick_menu_tab_hover). Since ATL can't branch, the tab
## screen picks between two transforms on a quick_menu_hover store variable and
## restarts the interaction when it flips.

init python:
    class QuickMenuToggle(Action):
        """
        Opens or closes the quick menu panel, sliding it in and out.
        """
        def __call__(self):
            store.quick_menu_open = not store.quick_menu_open

            ## No zorder kwarg here on purpose: show_screen's parameter is
            ## _zorder, and any keyword that doesn't start with an underscore
            ## gets forwarded to the screen as a constructor argument -- which
            ## this argument-less screen rejects. The screen sets its own
            ## zorder in its body instead.
            if store.quick_menu_open:
                renpy.show_screen("quick_menu_panel")
            else:

                ## Clear the hover flag on close. While the panel is open the
                ## closed-tab button doesn't exist, so it can't fire unhovered;
                ## and when it's re-created on close, a button the cursor isn't
                ## over never gains focus in the first place and so never fires
                ## unhovered either. Left alone, a True from the click that
                ## opened the panel would stick, and the closed tab would stay
                ## drawn in its leaned branch forever.
                store.quick_menu_hover = False

                renpy.hide_screen("quick_menu_panel")

            renpy.restart_interaction()


## The always-visible tab in its closed, un-hovered position: art at
## x 1258..1302, y 52..154.
##
## ypos 40 puts the tab flush below the top cinematic bar, which is
## Solid("#000000") at y 0..40 (see screen cinematic_bars). The tab can't sit
## over it because quick_menu sets zorder 100 while cinematic_bars has no
## zorder and so draws underneath -- the tab would just cover the bar.
##
## xoffset 22 halves the tab off the right edge: the art is 44px wide, so only
## its left 22px (screen x 1258..1280) is on screen and the other half hangs
## off at x 1280..1302.
transform quick_menu_tab_closed:
    xalign 1.0
    ypos 40
    xoffset 22

## The same tab while hovered: art at x 1236..1280, all 44px on screen.
##
## The lean is a transform on the *button*, not on a hover image, and that
## matters. An earlier version used
## "hover Transform('...', xoffset=-22)", which slid the picture 22px left
## inside an 81x121 button box: the art moved but the box didn't, and
## focus_mask (which resolves to the button's current render, so it follows the
## image rather than the button) left art and hitbox disagreeing -- a
## ghosted/doubled look. Moving the transform onto the button keeps the
## picture, the box and the clickable region in lockstep, so the whole moved
## button is clickable.
##
## xoffset 0 rather than -22 is deliberate: this is an absolute position, and
## 0 is what puts the art's right edge on the screen edge at 1280.
transform quick_menu_tab_hover:
    xalign 1.0
    ypos 40
    xoffset 0

## The panel. 273 is the cropped canvas width, so xoffset 273 parks it entirely
## off screen to the right.
##
## ypos 36 top-aligns the panel art with the tab art: the panel art starts at
## canvas y 16 (36 + 16 = 52) and the tab art starts at canvas y 12 (40 + 12 =
## 52), so both begin on the same scanline.
transform quick_menu_panel_anim:
    xalign 1.0
    ypos 36

    xsize 273
    ysize 436

    on show:
        xoffset 273
        linear 0.20 xoffset 0

    on hide:
        xoffset 0
        linear 0.20 xoffset 273


## Overlay screen: the closed tab, plus the quick_menu/main_menu gating.
##
## Registered in config.overlay_screens (see options.rpy) rather than pulled in
## with "use" from the say/nvl screens. The say screen is rebuilt for every
## line of dialogue, which would restart the animations above and make the
## panel slide in again on each line. As an overlay it persists.
screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    ## not main_menu keeps this off the main menu and off the Load/About/
    ## Preferences screens, which are all "menu" screens reached via ShowMenu.
    ## not quick_menu_open hides the closed tab entirely once the panel is
    ## open, so pressing it makes it vanish rather than slide.
    if quick_menu and not main_menu and not quick_menu_open:

        ## Two near-identical buttons rather than one button with a shifted
        ## hover image. Only the "at" line differs; see
        ## quick_menu_tab_hover for why the lean lives on the button.
        ##
        ## There's no "hover" displayable, so idle is the only image and the
        ## position change *is* the hover feedback. focus_mask True then masks
        ## against whichever button is currently drawn, so picture, box and
        ## clickable region always agree.
        ##
        ## The transform is picked with an "if", which only re-evaluates when
        ## an interaction restarts. SetVariable does that itself -- the data
        ## actions call renpy.restart_interaction() in their __call__ -- so no
        ## explicit restart is needed here.
        ##
        ## No padding on either: an imagebutton's natural hitbox is already its
        ## full 81x121 canvas, which is what focus_mask wants. Adding
        ## xpadding/ypadding would grow the button and offset the child image
        ## inward, leaving a visible gap at the right screen edge.
        if quick_menu_hover:

            imagebutton:

                idle "gui/button/menu/side button.png"
                focus_mask True

                at quick_menu_tab_hover

                action QuickMenuToggle()

                unhovered SetVariable("quick_menu_hover", False)

        else:

            imagebutton:

                idle "gui/button/menu/side button.png"
                focus_mask True

                at quick_menu_tab_closed

                action QuickMenuToggle()

                hovered SetVariable("quick_menu_hover", True)


## The expanded panel. Shown/hidden by QuickMenuToggle.
screen quick_menu_panel():

    zorder 100

    ## xalign/ypos live in quick_menu_panel_anim, not here -- a transform
    ## applied with "at" overrides the same properties set on the displayable.
    fixed:

        at quick_menu_panel_anim

        xsize 273
        ysize 436

        ## The shipped PNG is a full 1280x720 export. The panel body sits at
        ## x 1084..1279, y 99..490, with the collapse tab protruding to its
        ## left at x 1039..1086, y 106..212. Crop it (x, y, w, h) to a 273x436
        ## canvas: 32px of left padding, the 47px tab, then the 194px body,
        ## right-aligned on the art's right edge. In these local coordinates
        ## the body spans x 77..272, y 19..410 and the tab x 32..79, y 26..132.
        add Transform("gui/button/menu/quick_menu.png", crop=(1007, 80, 273, 436))

        ## Invisible hotspot over the tab baked into the art (local
        ## x 32..79, y 26..132): this is the collapse control. background None
        ## keeps it from drawing anything; there's no hover artwork, so the
        ## button pointer and the focus outline are the only feedback.
        button:

            xpos 32
            ypos 26
            xysize (47, 107)

            background None

            action QuickMenuToggle()

        ## Centred in the panel body: the body spans local x 77..272, so a
        ## 170-wide column sits at xpos 77 + (196 - 170) / 2 = 89. This also
        ## keeps the column clear of the tab hotspot on its left.
        ##
        ## ypos 40 leaves 21px between the column and the panel body's top edge
        ## (local y 19), and ysize 355 runs it down to local y 395, short of
        ## the body's bottom edge at 410.
        ##
        ## spacing 14 is deliberately loose enough to read as separate buttons
        ## but tight enough to keep the column compact. The vbox is top-aligned,
        ## so with 8 buttons at 14px gaps the column no longer reaches ysize
        ## 355 and the panel has empty space below it -- lower ysize here won't
        ## move anything, since a vbox lays its children out from the top.
        vbox:

            style_prefix "quick"

            xpos 89
            ypos 40
            xsize 170
            ysize 355

            spacing 14

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            textbutton _("Q.Save") action QuickSave()
            textbutton _("Q.Load") action QuickLoad()
            textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface. Registered in
## options.rpy alongside cinematic_bars.
# init python:
#     config.overlay_screens.append("quick_menu")

## quick_menu controls whether the tab is shown at all. It's set by the say,
## choice and nvl screens, so the tab doesn't cover a choice's options.
default quick_menu = True

## Whether the quick menu panel is expanded. Toggled by the side button.
default quick_menu_open = False

## Whether the side button is hovered. Swaps the tab between
## quick_menu_tab_closed and quick_menu_tab_hover, so the lean moves the
## button's box and hitbox along with its art. ATL has no "if" statement, so
## this has to be a store variable the screen branches on rather than
## something a transform can react to.
default quick_menu_hover = False

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

    ## These buttons are stacked vertically inside a painted panel, so the
    ## stock horizontal-strip background would tile across it. Drop the
    ## background and give each button the panel's inner width instead.
    background None
    xfill False
    xsize 170

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    text_align 0.5
    xalign 0.5


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    if main_menu:

        ## The main menu uses painted button art instead of text buttons.
        ##
        ## The source art (gui/button/start1.png and friends) is a full
        ## 1280x720 canvas with a single button painted at an absolute
        ## position. The mm_*_idle and mm_*_hover images are those canvases
        ## cropped to just the painted pill, positioned here with xpos/ypos.
        ##
        ## Idle and hover are cropped to the same rect on purpose. The hover art
        ## is drawn slightly larger and shifted up-left, so cropping each state
        ## to its own bounds would resize the button on hover and make it
        ## jitter. Sharing one rect keeps the button a fixed size and preserves
        ## the grow-from-the-top-left effect as painted.
        ##
        ## This is a child of the screen rather than of the navigation vbox, so
        ## that xpos/ypos are relative to the screen origin the art was painted
        ## against. The coordinates are absolute and assume gui.init(1280, 720).
        fixed:

            xpos 0
            ypos 0

            xsize 1280
            ysize 720

            ## focus_mask makes the transparent area around each rounded pill
            ## non-clickable, so the rectangular crop box does not create stray
            ## hot spots at the corners. It is set here rather than through a
            ## style: style_prefix combines with each child's own default style
            ## name, so a prefix of "mm_image_button" would resolve to the
            ## undefined "mm_image_button_image_button" and silently do nothing.
            ##
            ## Order matches the painted column, top to bottom.

            imagebutton:
                idle "gui/button/mm_start_idle.png"
                hover "gui/button/mm_start_hover.png"
                focus_mask True
                xpos 60
                ypos 328
                action Start()

            imagebutton:
                idle "gui/button/mm_load_idle.png"
                hover "gui/button/mm_load_hover.png"
                focus_mask True
                xpos 77
                ypos 420
                action ShowMenu("load")

            imagebutton:
                idle "gui/button/mm_about_idle.png"
                hover "gui/button/mm_about_hover.png"
                focus_mask True
                xpos 87
                ypos 496
                action ShowMenu("about")

            imagebutton:
                idle "gui/button/mm_options_idle.png"
                hover "gui/button/mm_options_hover.png"
                focus_mask True
                xpos 89
                ypos 557
                action ShowMenu("preferences")

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web. The art has no mobile variant.
            if renpy.variant("pc"):

                imagebutton:
                    idle "gui/button/mm_quit_idle.png"
                    hover "gui/button/mm_quit_hover.png"
                    focus_mask True
                    xpos 79
                    ypos 621
                    action Quit(confirm=not main_menu)

    else:

        vbox:
            style_prefix "navigation"

            xpos gui.navigation_xpos
            yalign 0.5

            spacing gui.navigation_spacing

            ## We're using the Separated History Screen, so we'll comment this out
            # textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

            textbutton _("Load") action ShowMenu("load")

            textbutton _("Preferences") action ShowMenu("preferences")

            if _in_replay:

                textbutton _("End Replay") action EndReplay(confirm=True)

            else:

                textbutton _("Main Menu") action MainMenu()

            textbutton _("About") action ShowMenu("about")

            if renpy.variant("pc"):

                ## The quit button is banned on iOS and unnecessary on Android
                ## and Web.
                textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    ## Decorative border frame. Screen children are drawn in source order with
    ## later ones on top, so this composites over the background art, and the
    ## navigation screen below stays on top of it.
    ##
    ## Note that the left panel of this frame is opaque for the full screen
    ## height (roughly x 0..400, bulging with y), so it covers that part of the
    ## background art, and the button column sits on solid red.
    add "gui/button/menu/menu frame.png"

    ## Replaces the [config.name] title text that used to sit in the bottom
    ## right. logo.png is a full 1280x720 canvas with the logo painted at the
    ## top left (x 38..367, y 34..294), so it is added uncropped and lands where
    ## it was painted rather than in the corner.
    ##
    ## It goes after the frame because the frame is opaque in that region, so
    ## adding it first would hide the logo.
    add "gui/button/menu/logo.png"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    ## Personally, I usually make a separate set of menu buttons so I can
    ## control placement better.
    use navigation


style main_menu_frame is empty

style main_menu_frame:
    xsize 280
    yfill True

    background "gui/overlay/main_menu.png"


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    ## Semi-transparent green wash so the Load/About/Preferences content reads
    ## clearly on top of the main menu art. Drawn after the background but
    ## before the frames, so the navigation button column below stays crisp.
    if main_menu:
        add Solid("#0b3d0b80")

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    ## Only shown for menus opened from inside the game. On the main menu's
    ## Load/About/Preferences screens this is hidden -- ESC already returns to
    ## the main menu via the key "game_menu" action below.
    if not main_menu:
        textbutton _("Return"):
            style "return_button"

            action Return()



    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    ## These paddings set the height of the area the game menu content is laid
    ## out in (Load/Save slots, About, Preferences, History). They were reduced
    ## from 45/180 because the 3x2 slot grid is ~422px tall and, in the old
    ## 485px-tall area, the grid only cleared the page-name field and the page
    ## nav row by ~1px. 50px more room now gives ~20px above and below the
    ## grid. The grid re-centers itself via yalign, so no change is needed in
    ## screen file_slots. Note this shifts the About/Preferences content up by
    ## ~17px; the "Load"/"About" title on the left is positioned by
    ## game_menu_label and does not move.
    bottom_padding 30
    top_padding 145

    ## This used to dim the whole game menu screen. It's now just transparent,
    ## so the main menu art shows through the Load/Preferences/About screens.
    ## Don't delete the frame in screen game_menu -- this style also supplies
    ## the top/bottom padding those screens are laid out with. The green wash
    ## over the main menu art is added in screen game_menu instead, so leave
    ## this background commented out unless you want a second overlay.
    # background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


## Set these to false if you wish to remove the Auto or Quick file pages
define config.has_autosave = True
define config.has_quicksave = True

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    size 20
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    size 18
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    size 14
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Custom Preferences here. Additional vboxes of type
                ## "radio" or "check" can be added to add creator-defined
                ## preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")


                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 450


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

## Note: This is a custom version of the History screen that is not attached
## to the game menu. It draws the log directly onto history.png with no frame,
## title, or scrollbar; mousewheel and drag scroll it. The panel geometry is
## described on the screen below, and gui.history_text_width in gui.rpy sets
## the wrapped text column.

screen history():

    tag menu

    predict False

    ## The art is a full 1280x720 canvas whose painted panel occupies
    ## x 745..1279 for the full screen height, with a curved left edge. It's
    ## added uncropped so the panel lands against the right edge and the game
    ## stays visible to its left. This isn't a Frame because the panel's shape
    ## is baked into the image, not tiled.
    add "gui/button/menu/history.png"

    ## The log is drawn directly on the panel art: a backgroundless frame
    ## supplies the panel-width column and its 40px inner padding, and a
    ## viewport scrolls inside it. The vertical scrollbar is what builds the
    ## `side` layout that bounds the viewport, so it must stay even though it's
    ## styled to be subtle (see style history_vscrollbar). No frame background
    ## or title.
    frame:

        style_prefix "history"

        background None

        xalign 1.0
        xsize 535
        xmargin 0

        ysize 640
        ypos 40

        ## xpadding sets left and right padding to the same value (the panel's
        ## 455px inner width is 535 - 2*40; the scrollbar and its 4px spacing
        ## take 12px of that, so the text column is 443 -- see
        ## gui.history_text_width).
        xpadding 40

        ## ypadding sets top and bottom padding to the same value.
        ypadding 40

        viewport:

            yinitial 1.0

            scrollbars "vertical"
            mousewheel True
            draggable True
            pagekeys True
            arrowkeys True

            ## Fill the frame's inner height so the viewport is bounded and
            ## scrolls, instead of growing to fit the whole log.
            side_yfill True
            side_spacing 4

            vbox:

                for h in _history_list:

                    ## Each entry stacks the character name on its own line
                    ## above the dialogue, so both span the full text column.
                    vbox:

                        spacing 4

                        if h.who:

                            label h.who:
                                style "history_name"
                                substitute False

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            line_spacing 5
                            substitute False

                    ## This puts some space between entries so it's easier to read
                    null height 20

                if not _history_list:

                    text "The text log is empty." line_spacing 10
                    ## Adding line_spacing prevents the bottom of the text
                    ## from getting cut off. Adjust when replacing the
                    ## default fonts.

        ## No Return button -- history.png is a right-hand panel, and ESC (or
        ## the quick menu's History button) closes this screen.

### The old version of the History screen, just for reference.
# screen history():

#     tag menu

#     ## Avoid predicting this screen, as it can be very large.
#     predict False

#     use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

#         style_prefix "history"

#         for h in _history_list:

#             window:

#                 ## This lays things out properly if history_height is None.
#                 has fixed:
#                     yfit True

#                 if h.who:

#                     label h.who:
#                         style "history_name"
#                         substitute False

#                         ## Take the color of the who text from the Character, if
#                         ## set.
#                         if "color" in h.who_args:
#                             text_color h.who_args["color"]

#                 $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
#                 text what:
#                     substitute False

#         if not _history_list:
#             label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt" }


## History styles. Each entry is a vbox (see screen history): the character
## name sits on its own line above the dialogue, both left-aligned in the
## panel's text column. Only the dialogue needs a width, since it wraps.
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_name:
    xalign 0.0

style history_name_text:
    text_align 0.0
    color "#686565"
    font "gui/font/baskervville.regular.ttf"

style history_text:
    xsize gui.history_text_width
    text_align gui.history_text_xalign
    layout "tex"
    color "#404040"
    font "gui/font/baskervville.regular.ttf"

## The vertical scrollbar the viewport in screen history builds. style_prefix
## "history" on the frame names it history_vscrollbar. Kept deliberately subtle
## -- a slim, translucent thumb over a near-invisible track -- and hidden
## entirely when the log fits (unscrollable "hide").
style history_vscrollbar:
    xsize 8
    base_bar Solid("#003d5126")
    thumb Solid("#02070899")
    unscrollable "hide"


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    ## NVL shows dialogue and its menu on the same screen, so the quick menu
    ## tab is only shown when there's no menu (items is None) to sit over.
    $ quick_menu = (items is None)

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        vbox:
            spacing 5
            xfill True

        if who is not None:
            text who:
                id "who"
                style "bubble_who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.0
    textalign 0.0
    yoffset -35
    size 25
    color "#f5f5f5"
    font "gui/font/baskervville.regular.ttf"

style bubble_what:
    xalign 0.5
    text_align 0.5
    layout "subtitle"
    color "#f5f5f5"
    font "gui/font/baskervville.regular.ttf"


define bubble.frame = Frame("gui/text box.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, alpha=0),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, alpha=0),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, alpha=0),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, alpha=0),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : Transform(bubble.thoughtframe, alpha=0.0),
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses the same side-button tab and panel, but with fewer and bigger
## buttons that are easier to touch. The panel art is the same size, so the
## larger buttons are laid out in a two-column grid instead of a single stack.
screen quick_menu():
    variant "touch"

    zorder 100

    ## Same guard, transform and hover branching as the desktop version -- see
    ## the comments on screen quick_menu above. Only the closed tab lives here;
    ## the panel is a separate screen shown/hidden by QuickMenuToggle, and it
    ## carries its own baked-in collapse hotspot.
    if quick_menu and not main_menu and not quick_menu_open:

        if quick_menu_hover:

            imagebutton:

                idle "gui/button/menu/side button.png"
                focus_mask True

                at quick_menu_tab_hover

                action QuickMenuToggle()

                unhovered SetVariable("quick_menu_hover", False)

        else:

            imagebutton:

                idle "gui/button/menu/side button.png"
                focus_mask True

                at quick_menu_tab_closed

                action QuickMenuToggle()

                hovered SetVariable("quick_menu_hover", True)


## The panel art is the same size on touch, so the larger touch-sized buttons
## go in a 2-column grid instead of a single stack.
##
## 3 rows, not 2: a fixed "grid 2 2" only has 4 cells, so the fifth button
## (Save) was silently dropped and never appeared on touch layouts.
screen quick_menu_panel():
    variant "touch"

    zorder 100

    fixed:

        at quick_menu_panel_anim

        xsize 273
        ysize 436

        ## Same crop as the desktop panel -- see the comments there.
        add Transform("gui/button/menu/quick_menu.png", crop=(1007, 80, 273, 436))

        ## Same collapse hotspot over the tab baked into the art as the desktop
        ## panel -- see the comments there.
        button:

            xpos 32
            ypos 26
            xysize (47, 107)

            background None

            action QuickMenuToggle()

        grid 2 3:

            style_prefix "quick"

            ## Same vertical band and centring as the desktop column (xpos 89
            ## centres 170px in the panel body's local x 77..272): local y 40
            ## down to the body's bottom edge at 410. Touch buttons use the
            ## larger gui.quick_button_text_size (30), so 20px gaps keep the
            ## same visual separation the desktop's 14px gives at size 14.
            xpos 89
            ypos 40
            xsize 170
            ysize 355

            spacing 20

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')


style window:
    variant "small"
    background "gui/phone/text box.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    # background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
