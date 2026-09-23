################################################################################
##
## Color Picker for Ren'Py by Feniks (feniksdev.itch.io / feniksdev.com) v1.4
##
################################################################################
## This file contains code for a controller-compatible color picker in Ren'Py.
## If you use this code in your projects, credit me as Feniks @ feniksdev.com
## It requires https://feniksdev.itch.io/controller-support-expansion-for-renpy
## in order to work.
##
## The code at the top of this file is backend to set up controller
## compatibility, and then there is a screen declaration and a test label to
## demonstrate the picker. You can `jump test_controller_picker` somewhere in
## your script to test it out.
##
## Leave a comment on the tool page on itch.io or an issue on the GitHub
## if you run into any issues.
## https://feniksdev.itch.io/color-picker-for-renpy
## https://github.com/shawna-p/renpy-color-picker
################################################################################
## BACKEND
################################################################################
init python:

    class PickerHueValue(BarValue):
        """
        A special BarValue subclass which responds to stick events on the
        provided axis. Used to hook into bars to adjust the hue of the
        color picker with controller sticks.

        Attributes:
        -----------
        picker : ColorPicker
            The color picker whose hue is being adjusted.
        which_axis : string
            One of 'x' or 'y', correlating to which axis this bar is adjusting.
            vbar should use 'y' and bar should use 'x'. This matches the stick
            movements to the bar adjustment.
        stick_event : StickEvent
            A StickEvent used to track movement of the sticks for controlling
            the bar.
        """
        def __init__(self, picker, which_axis='x', **kwargs):
            self.picker = picker
            self.which_axis = which_axis
            kwargs['event_type'] = 'range'
            kwargs['which_stick'] = kwargs.get('which_stick', 'left')
            kwargs['speed'] = kwargs.get('speed', 0.5)
            kwargs['x_min'] = 0.0
            kwargs['x_max'] = 1.0
            kwargs['y_min'] = 0.0
            kwargs['y_max'] = 1.0
            kwargs['start_x'] = picker.hue_rotation
            kwargs['start_y'] = picker.hue_rotation
            kwargs['changed'] = self.rotate_picker_hue
            self.stick_event = StickEvent(**kwargs)
            ## Ensure this bar is still clickable with the mouse, too
            self.stick_event._x.changed = self.set_value
            self.stick_event._x.adjustable = True
            self.stick_event._y.changed = self.set_value
            self.stick_event._y.adjustable = True
            super(PickerHueValue, self).__init__()

        def rotate_picker_hue(self, x, y, stick):
            """A stick callback which updates the picker's hue rotation."""
            if self.which_axis == 'x':
                self.picker.hue_rotation = float(x)
                self.stick_event._y._value = self.stick_event.x
            else:
                self.picker.hue_rotation = float(y)
                self.stick_event._x._value = self.stick_event.y

        def get_adjustment(self):
            """Return the appropriate stick adjustment that controls the hue."""
            if self.which_axis == 'x':
                return self.stick_event._x
            else:
                return self.stick_event._y

        def periodic(self, st):
            """Refreshes the adjustments based on stick movement."""
            self.stick_event.handle_stick_movement(reset_deadzone=False)
            if self.stick_event.newly_in_deadzone:
                ## Update the screen when the sticks stop.
                renpy.restart_interaction()
                self.stick_event.newly_in_deadzone = False
            return self.stick_event.refresh_rate
        def get_value(self):
            return self.picker.hue_rotation
        def set_value(self, value):
            self.picker.hue_rotation = value

    class PickerStickEvent(StickEvent):
        """
        A class which controls a color picker using controller stick input.
        Takes all the arguments StickEvent does; most notably which_stick and
        speed.
        """
        def __init__(self, picker, **kwargs):
            self.picker = picker
            kwargs['start_x'] = picker.selector_xpos
            kwargs['start_y'] = picker.selector_ypos
            kwargs['x_min'] = 0.0
            kwargs['x_max'] = 1.0
            kwargs['y_min'] = 0.0
            kwargs['y_max'] = 1.0
            kwargs['event_type'] = 'range'
            kwargs['speed'] = kwargs.get('speed', 1.0)
            kwargs['changed'] = self.update_picker
            kwargs['which_stick'] = kwargs.get('which_stick', 'right')
            super(PickerStickEvent, self).__init__(**kwargs)

        def update_picker(self, x, y, stick):
            """
            Update the color picker selector position based on the stick
            position values.
            """
            relative_x = float(x)
            relative_y = float(y)

            in_range = (0.0 <= relative_x <= 1.0) and (0.0 <= relative_y <= 1.0)
            self.picker.selector_xpos = relative_x
            self.picker.selector_ypos = relative_y
            ## Limit x/ypos and update the selector position
            self.picker.selector_xpos = min(max(self.picker.selector_xpos, 0.0), 1.0)
            self.picker.selector_ypos = min(max(self.picker.selector_ypos, 0.0), 1.0)
            ## Update the hue based on the selector position
            self.picker.update_hue()

            return None

        def handle_stick_movement(self, reset_deadzone=True):
            """
            Handles stick movement and ensures that the screen is refreshed
            when the stick stops moving (since we aren't clicking and dragging
            to run a refresh on mouse release).
            """
            super(PickerStickEvent, self).handle_stick_movement(reset_deadzone=False)
            if self.newly_in_deadzone:
                ## Update the screen when the sticks stop.
                renpy.restart_interaction()
                if self.picker.mouseup_callback is not None:
                    renpy.run(self.picker.mouseup_callback, self.picker)
                return
            if self.newly_in_deadzone and reset_deadzone:
                self.newly_in_deadzone = False

################################################################################
## SCREENS
################################################################################
screen color_picker_controller():

    ## The picker itself. Its size is 600x600 with the starting colour #ff8335.
    ## You may declare this outside of the screen to make it easier to access;
    ## see color_picker_v2 for an example of this.
    default picker = ColorPicker(600, 600, "#ff8335")
    ## This is required so the stick can move the picker around the colour area.
    default stick_events = PickerStickEvent(picker)

    style_prefix 'ccpicker' ## Simplifies some of the style property code

    add "#21212d" ## The background

    hbox:
        ## A vertical bar which lets you change the hue of the picker.
        ## You should only have one of vbar or bar to adjust the picker hue.
        ## This uses the special PickerHueValue, which hooks into controller
        ## stick movement.
        vbar value PickerHueValue(picker, which_axis='y')

        vbox:
            ## The picker itself
            add picker
            ## A horizontal bar that lets you change the hue of the picker.
            ## You should only have one of vbar or bar to adjust the picker hue.
            # bar value PickerHueValue(picker, which_axis='x')
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
            ## These update when the screen is refreshed
            ## since they aren't a dynamic displayable
            text "R: [picker.color.rgb[0]:.2f]"
            text "G: [picker.color.rgb[1]:.2f]"
            text "B: [picker.color.rgb[2]:.2f]"

    ## Add the PickerStickEvent from earlier so the controller sticks will
    ## move the color picker selector around
    add stick_events

    ## In this case, the screen returns the picker's colour. The colour itself
    ## is always stored in the picker's `color` attribute.
    textbutton "Return" action Return(picker.color) align (1.0, 1.0):
        ## Make sure that hitting cancel will return from this screen
        keysym pad_config.get_event("cancel") keyboard_focus False

################################################################################
## TESTING LABEL
################################################################################
label test_controller_picker():
    call screen color_picker_controller()
    $ chosen_color = _return.hexcode
    ## This is used to put the returned colour into a colour text tag
    $ color_tag = "{color=%s}" % chosen_color
    "[color_tag]You chose the colour [chosen_color].{/color}"
    return

################################################################################
## Styles
style ccpicker_vbox:
    align (0.5, 0.5)
    spacing 25
style ccpicker_hbox:
    align (0.5, 0.5)
    spacing 25
style ccpicker_vbar:
    xysize (50, 600)
    ## Unlike the other examples, we invert this so it goes from 0 (top) to 1
    ## (bottom) so the stick movement lines up properly
    bar_invert True
    base_bar Transform(
        At(Transform("#000", xysize=(50, 600)), spectrum(horizontal=False)),
        yzoom=-1)
    thumb Transform("selector_bg", xysize=(50, 20))
    thumb_offset 10
style ccpicker_bar:
    xysize (600, 50)
    base_bar At(Transform("#000", xysize=(600, 50)), spectrum())
    thumb Transform("selector_bg", xysize=(20, 50))
    thumb_offset 10
style ccpicker_text:
    color "#fff"
style ccpicker_button:
    padding (4, 4) insensitive_background "#fff"
style ccpicker_button_text:
    color "#aaa"
    hover_color "#fff"
style ccpicker_image_button:
    xysize (108, 108)
    padding (4, 4)
    hover_foreground "#fff3"
    selected_background "#fff"
