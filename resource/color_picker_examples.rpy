################################################################################
##
## COLOR PICKER EXAMPLES v1.4
##
################################################################################
## To quickly test these examples in your game, jump to the label
## how_to_use_color_picker i.e.
# jump how_to_use_color_picker

################################################################################
## IMAGES
################################################################################
## In order to avoid including unnecessary image files, the default version of
## these images constructs an image in code. You may, however, want to change
## it. The following code is provided as an example of how to do so.

## Used for both the spectrum thumb and the colour indicator. Can be changed.
# image selector_bg = Frame("selector.webp", 5, 5)

## The image used for the indicator showing the current colour.
# image selector = Transform("selector_bg", xysize=(15, 15))

################################################################################
## SCREENS
################################################################################
## EXAMPLE 1
## A sample screen to demonstrate the colour picker.
## Simply write `call screen color_picker()` to test it.
screen color_picker():

    ## The picker itself. Its size is 600x600 with the starting colour #ff8335.
    ## You may declare this outside of the screen to make it easier to access;
    ## see color_picker_v2 for an example of this.
    default picker = ColorPicker(600, 600, "#ff8335")

    style_prefix 'cpicker' ## Simplifies some of the style property code

    add "#21212d" ## The background

    hbox:
        ## A vertical bar which lets you change the hue of the picker.
        vbar value FieldValue(picker, "hue_rotation", 1.0)

        vbox:
            ## The picker itself
            add picker
            ## A horizontal bar that lets you change the hue of the picker
            bar value FieldValue(picker, "hue_rotation", 1.0)
        vbox:
            xsize 200 spacing 10 align (0.0, 0.0)
            ## The swatch. Provided by the ColorPicker. It updates in real-time.
            add picker.swatch(xsize=100, ysize=100)

            ## You can display other information on the color here, as desired
            ## Some examples are provided. Note regular screen elements only
            ## update when the mouse is released, instead of in real-time. You
            ## will need to use a DynamicDisplayable for real-time updates.
            ## The hexcode is automatically provided as part of the picker
            ## class as a DynamicDisplayable that updates in real-time
            add picker.hexcode(style='picker_hexcode')
            ## These update when the mouse button is released
            ## since they aren't a dynamic displayable
            text "R: [picker.color.rgb[0]:.2f]"
            text "G: [picker.color.rgb[1]:.2f]"
            text "B: [picker.color.rgb[2]:.2f]"

    ## In this case, the screen returns the picker's colour. The colour itself
    ## is always stored in the picker's `color` attribute.
    textbutton "Return" action Return(picker.color) align (1.0, 1.0)

################################################################################
## Styles
style cpicker_vbox:
    align (0.5, 0.5)
    spacing 25
style cpicker_hbox:
    align (0.5, 0.5)
    spacing 25
style cpicker_vbar:
    xysize (50, 600)
    base_bar At(Transform("#000", xysize=(50, 600)), spectrum(horizontal=False))
    thumb Transform("selector_bg", xysize=(50, 20))
    thumb_offset 10
style cpicker_bar:
    xysize (600, 50)
    base_bar At(Transform("#000", xysize=(600, 50)), spectrum())
    thumb Transform("selector_bg", xysize=(20, 50))
    thumb_offset 10
style cpicker_text:
    color "#fff"
style cpicker_button:
    padding (4, 4) insensitive_background "#fff"
style cpicker_button_text:
    color "#aaa"
    hover_color "#fff"
style cpicker_image_button:
    xysize (108, 108)
    padding (4, 4)
    hover_foreground "#fff3"
    selected_background "#fff"

################################################################################
## EXAMPLE 2
## The picker itself. This one is declared outside of the screen.
default picker2 = ColorPicker(600, 600, "#f93c3e",
    ## This sets up two saved colours for the picker. These can be accessed
    ## later to allow the picker to swap between two different colours.
    ## You could add more keys and default colours, if desired. The keys don't
    ## have to be numbers, either; they could be names like "background".
    saved_colors={0 : "#f93c3e", 1 : "#ff8335"},
    ## This sets up the first dictionary key as the "current" colour at
    ## the start. It will be updated automatically later.
    last_saved_color=0)

screen color_picker_v2():

    style_prefix 'cpicker'

    add "#21212d"

    hbox:
        ## A vertical bar which lets you change the hue of the picker.
        vbar value FieldValue(picker2, "hue_rotation", 1.0)

        ## The picker itself
        vbox:
            add picker2
            ## A horizontal bar that lets you change the hue of the picker
            bar value FieldValue(picker2, "hue_rotation", 1.0)

        vbox:
            xsize 200 spacing 10 align (0.0, 0.0)
            ## The following code lets you switch between
            ## two different swatches to choose more than one colour. The 0
            ## and 1 keys were set up in the picker2 declaration.
            for color_key in [0, 1]:
                imagebutton:
                    ## This fetches the colour from the picker's saved
                    ## dictionary according to the passed-in key. You can
                    ## provide a size as well.
                    idle picker2.swatch(color_key, xsize=100, ysize=100)
                    ## This action saves the last used colour to the picker,
                    ## then updates the key to the provided one and
                    ## redraws that saved colour to the screen.
                    action picker2.SwapToSavedColor(color_key)

            ## The hex code
            add picker2.hexcode(style='picker_hexcode')
            ## The RGB values
            text "R: [picker2.color.rgb[0]:.2f]"
            text "G: [picker2.color.rgb[1]:.2f]"
            text "B: [picker2.color.rgb[2]:.2f]"

    ## We don't have to return the picker because picker2 was declared as
    ## a global variable outside of the screen.
    textbutton "Return" align (1.0, 1.0) action Return()

################################################################################
## EXAMPLE 3
## A sample screen to demonstrate the four corner colour picker.
## Simply write `call screen four_corner_picker()` to test it.
screen four_corner_picker():

    ## The picker itself. Its size is 600x600, and it's given a colour for
    ## all four corners (top right, bottom right, bottom left, top left)
    ## You may declare this outside of the screen to make it easier to access.
    default picker = ColorPicker(600, 600,
        four_corners=("#ff8335", "#f93c3e", "#292835", "#f7f7ed"))

    style_prefix 'cpicker'

    add "#21212d"

    hbox:
        spacing 25 align (0.5, 0.5)

        vbox:
            ## The picker itself
            add picker
            ## A horizontal bar that lets you change the hue of the picker
            ## For a four-corner picker, you may not need this.
            bar value FieldValue(picker, "hue_rotation", 1.0) base_bar "#fff"
        vbox:
            xsize 200 spacing 10 align (0.0, 0.0)
            ## The swatch. Updates in real-time
            add picker.swatch(xsize=100, ysize=100)

            ## The hex code, as a dynamic displayable so it updates in real-time.
            ## This is a built in property of the ColorPicker class.
            add picker.hexcode(style='picker_hexcode')
            ## The RGB values
            text "R: [picker.color.rgb[0]:.2f]"
            text "G: [picker.color.rgb[1]:.2f]"
            text "B: [picker.color.rgb[2]:.2f]"

    ## In this case, the screen returns the picker's colour. The colour itself
    ## is always stored in the picker's `color` attribute.
    textbutton "Return" action Return(picker.color) align (1.0, 1.0)

################################################################################
## EXAMPLE 4
## A sample screen to demonstrate the a colour picker which comes with a
## palette of pre-set colour options to pick from alongside allowing for
## freeform colour picking.
screen preset_color_picker():

    default picker = ColorPicker(600, 600, "#292835",
        ## This sets up two saved colours for the picker. These can be accessed
        ## later to allow the picker to swap between two different colours.
        ## You could add more keys and default colours, if desired.
        saved_colors={'left' : "#292835", 'right' : "#ff3a6a"},
        ## This sets up the first dictionary key as the "current" colour at
        ## the start. It will be updated automatically later.
        last_saved_color='left')

    style_prefix 'cpicker'
    add "#21212d"

    hbox:
        ## A vertical bar which lets you change the hue of the picker.
        vbar value FieldValue(picker, "hue_rotation", 1.0):
            yalign 1.0 yoffset -75

        vbox:
            hbox:
                ## The following code lets you switch between
                ## two different swatches to choose more than one colour:
                for color_key in ['left', 'right']:
                    imagebutton:
                        ## This fetches the colour from the picker's saved
                        ## dictionary according to the passed-in key.
                        idle picker.swatch(color_key, xsize=100, ysize=100)
                        ## This action saves the last used colour to the picker,
                        ## then updates the key to the provided one and
                        ## redraws it to the screen.
                        action picker.SwapToSavedColor(color_key)
                vbox:
                    spacing 10 align (0.0, 0.0) xsize 150
                    ## The RGB values
                    text "R: [picker.color.rgb[0]:.2f]"
                    text "G: [picker.color.rgb[1]:.2f]"
                    text "B: [picker.color.rgb[2]:.2f]"

            ## The picker itself
            add picker
            ## A horizontal bar that lets you change the hue of the picker
            bar value FieldValue(picker, "hue_rotation", 1.0)

        vbox:
            xsize 200 spacing 10 align (0.0, 0.0)

            ## The hexcode of the current colour. This is a DynamicDisplayable
            ## for the currently active colour, so it can update in real time
            add picker.hexcode(style='picker_hexcode')

            ## Several pre-set colour options
            for c in ("#ff3a6a", "#f93c3e", "#ff8335", "#E5BA54",
                    "#f7f7ed", "#292835", "#000"):
                imagebutton:
                    ## This just sets the idle image as the colour. The size is
                    ## already set up in the styles so it isn't massive.
                    idle c
                    ## This action sets the colour picker to the provided
                    ## colour and redraws it to the screen.
                    action picker.SetColor(c)

    ## We return the entire picker object so we can grab both colour names
    ## from its saved colours dictionary.
    textbutton "Return" align (1.0, 1.0) action Return(picker)

################################################################################
## TESTING LABEL
################################################################################
default chosen_color = "#8b0f55"
label how_to_use_color_picker():
    "Soon, you will be shown a colour picker."

    ## EXAMPLE 1
    call screen color_picker()
    ## The colour the picker returns is a Color object. It has a hexcode
    ## field to easily get the hexadecimal colour code.
    $ chosen_color = _return.hexcode
    ## This is used to put the returned colour into a colour text tag
    $ color_tag = "{color=%s}" % chosen_color
    "[color_tag]You chose the colour [chosen_color].{/color}"

    ## EXAMPLE 2
    "The next picker will let you select two different colours."
    call screen color_picker_v2()
    ## The get_color method lets you pass in the dictionary key and retrieve
    ## the colour saved in the picker at that key.
    $ chosen_color1 = picker2.get_color(0).hexcode
    $ color1_tag = "{color=%s}" % chosen_color1
    $ chosen_color2 = picker2.get_color(1).hexcode
    $ color2_tag = "{color=%s}" % chosen_color2
    "[color1_tag]The first colour was [chosen_color1],{/color}[color2_tag] and the second was [chosen_color2].{/color}"

    ## EXAMPLE 3
    "Next, you will be shown a four-corner colour picker."
    call screen four_corner_picker()
    $ chosen_color = _return.hexcode
    $ color_tag = "{color=%s}" % chosen_color
    "[color_tag]You chose the colour [chosen_color].{/color}"

    ## EXAMPLE 4
    "Finally you will be shown a colour picker with pre-set swatches to choose from."
    call screen preset_color_picker()
    $ chosen_color = _return
    $ color1_tag = "{color=%s}" % chosen_color.get_color('left').hexcode
    $ chosen_color1 = chosen_color.get_color('left').hexcode
    $ color2_tag = "{color=%s}" % chosen_color.get_color('right').hexcode
    $ chosen_color2 = chosen_color.get_color('right').hexcode

    "[color1_tag]The left colour was [chosen_color1],{/color}[color2_tag] and the right was [chosen_color2].{/color}"
    return
