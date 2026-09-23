### Transitions ###
##
## A list of defined transitions to make it easier to use.
################################################################
# Ctr+F to find what you need
### TABLE OF CONTENTS ###
##
## 1. Move Transforms 
## 2. Rotate Transforms 
## 3. Action Transforms


################################################################

### 1. Move Transforms ###
# Below contains a list of all simple move transforms
# A move most def exists in Ren'Py but I'd prolly have to type out xalign...etc. I'm lazy so...
# All sprites start from left
# use x/yoffset to fit with any sprite pos

# default anchor for all sprites
define im_anchor = (0.5, 1.0)


# size: 800 x 1000
image oli = Transform("Oliver_Sprite.png", anchor=im_anchor)


# Simple move Left, Right, Up, Down with ease
# These two can be combined into moveXY but I use X more than Y, so it feels better to separate

# 'with move' already exists but you need 2 lines of code to use it and I'm lazy.
transform ts_moveX(dist, ts_speed=0.5):
    linear ts_speed xpos dist

# Same thing as above except with offset. 
transform ts_moveXoff(dist, ts_speed=0.5):
    linear ts_speed xoffset dist

# Simple move U/D with ease
transform ts_moveY(dist, ts_speed=0.5):
    linear ts_speed ypos dist

transform ts_moveYoff(dist, ts_speed=0.5):
    linear ts_speed yoffset dist

# Move back and forth using zoom
# Adjusts the sprite's height according to zoom value
# Adjust the multiplier to your needs.
transform ts_moveZ(dist, ts_speed=0.5):
    linear ts_speed zoom dist yoffset (-dist*100 if dist < 1.0 else (dist-1.0) * 750)

# You may need to adjust numbers depending on size of your sprite.
transform ts_moveinX(dist, ts_speed=0.5, start_pos=0-1200, f=False):
    xpos start_pos alpha (0.0 if f==True else 1.0)
    linear ts_speed xpos dist alpha (1.0 if f==True else 1.0)


transform ts_moveinY(dist, ts_speed=0.5, start_pos=0-1200, f=False):
    ypos start_pos alpha (0.0 if f==True else 1.0)
    linear ts_speed ypos dist alpha (1.0 if f==True else 1.0)

## Screen transforms
transform ts_moveinXScreen(start_pos, ts_speed=0.5, end_pos=0, f=False):
    on show:
        ts_moveinX(end_pos, ts_speed=ts_speed, start_pos=start_pos, f=f)
    on hide:
        ts_moveinX(start_pos, ts_speed=ts_speed, start_pos=end_pos, f=f)

transform ts_moveinYScreen(start_pos, ts_speed=0.5, end_pos=0, f=False):
    on show:
        ts_moveinY(end_pos, ts_speed=ts_speed, start_pos=start_pos, f=f)
    on hide:
        ts_moveinY(start_pos, ts_speed=ts_speed, start_pos=end_pos, f=f)


### 2. Rotate Tansforms ###
# instead of dist, we will use rot

# Regular rotation in 2D Space
transform ts_rot(rot=15, ts_speed=0.3):
    transform_anchor True
    ease ts_speed rotate rot

# Rotate in 3D Space
# https://www.renpy.org/doc/html/3dstage.html
transform ts_rotX(rot=15, ts_speed=0.3):
    ease ts_speed xrotate rot

# This is reliant on camera being active
transform ts_rotZ(rot=15, ts_speed=0.3):
    ease ts_speed yrotate rot 


# No rotTilt bc too many words
transform ts_tilt(xrot=0, yrot=0, ts_speed=0.3):
    linear ts_speed xrotate xrot yrotate yrot


# Basically rotXY, but dedicated to flipping
# 1 = Original orientation; -1 = Flipped

transform ts_flipX(rot=1, ts_speed=0.0):
    ease ts_speed xzoom (1 if rot >=0 else -1)

transform ts_flipY(rot=1, ts_speed=0.0):
    ease ts_speed yzoom (1 if rot >=0 else -1)

### 3. Action Transforms ###
# Below are "human actions" transforms like falling, jumping, etc
# Just thought it'd be fun

# Tip: Use with 'ts_moveZ()' for a cooler effect!
transform ts_acFall(ts_speed=0.2):
    easeout ts_speed yoffset config.screen_height + 1200
    

transform ts_acJump(dist, ts_speed=0.5):
    # reset
    yoffset 0
    easeout_quint ts_speed yoffset -abs(dist)
    pause(0.01)
    easein_quint ts_speed yoffset 0


transform ts_acBounce(dist, ts_speed=0.5, pt=0.3, rt=None):
    yoffset 0
    easeout_bounce ts_speed yoffset -abs(dist)
    easein_bounce  ts_speed yoffset 0
    pause(pt)
    repeat rt


# Tip: Use a lower 'dist' number for better effect!
transform ts_acShake(dist, ts_speed=0.5, rt=None):
    ease ts_speed xoffset dist
    ease ts_speed xoffset -dist
    repeat rt

transform ts_acSpin(ts_speed=0.5, xrot=0, xoff=0, yoff=0, rt=None): 
    parallel:
        linear 1.0 xrotate xrot xoffset xoff yoffset yoff
        
    parallel:
        yrotate 0
        linear 5.0 yrotate 360
        repeat rt


# Tip: Use with 'ts_tilt()' for a really funny effect!
transform ts_acPanicX(dist, ts_speed=0.5, rt=None):
    easeout_circ ts_speed xoffset dist
    xzoom -1.0 
    easeout_circ ts_speed xoffset -dist
    xzoom 1.0
    repeat

# Humans float...right?
transform ts_acFloat(dist, yoff=0, ts_speed=1.0, rot=0, rt=None):
    transform_anchor True
    parallel:
        ease ts_speed*2 rotate rot
        pause(0.3)
        ease ts_speed*2 rotate -rot
        pause(0.3)
        repeat
    parallel:
        easeout_quad ts_speed yoffset dist
        easein ts_speed yoffset 0 + yoff
        repeat


## Misc Transforms ##
# Transforms idk where to categorize

transform cam_reset:
    perspective True
    rotate 0 xrotate 0 yrotate 0 zrotate 0


### LABELS ################################################################

label tut_ts_moveXYZ:
    show oli at center
    "I will demonstrate in this order 'ts_moveX', 'ts_moveY', and then 'ts_moveZ'"
    "First with 'ts_moveX(dist, ts_speed=0.5)"
    show oli at ts_moveX(0.7)
    pause(1.0)
    show oli at ts_moveX(0.5)
    pause(1.0)
    "I should be back to my original position now."

    "I will do the same with 'ts_moveY(dist, ts_speed=0.5)'"
    show oli at ts_moveY(0.5)
    pause(1.0)
    show oli at ts_moveY(1.0)
    pause(1.0)

    show oli at center

    "Now 'ts_moveZ(dist, ts_speed=0.5)'"
    show oli at ts_moveZ(0.8)
    pause(1.0)
    show oli at ts_moveZ(4.0)
    pause(1.0)
    show oli at ts_moveZ(1.0)
    pause(1.0)
    show oli:
        zoom 1.0
    show oli at center

    "If you noticed with 'ts_moveZ', the sprite automatically adjusts it's height depending on whether it's closer or farther."
    "You may need to adjust the multiplier value for your sprites."
    "All 'ts_move' use these 2 parameters: dist and ts_speed."
    "For 'ts_moveZ()'  dist < 1.0 = further way; dist > 1.0 = closer. dist = 1.0 is original zoom position."

    "Now for the offset versions: 'ts_moveXoff(dist, ts_speed=0.5)"
    "-and 'ts_moveYoff(dist, ts_speed=0.5)."
    show oli at ts_moveXoff(384)
    pause(1.0)
    show oli at ts_moveXoff(0)
    pause(1.0)
    show oli at ts_moveYoff(540)
    pause(1.0)
    show oli at ts_moveYoff(0)
    pause(1.0)

    # in case of skip
    show oli:
        yoffset 0
        xoffset 0
    "The only difference between this and earlier is that these use 'xoffset' and 'yoffset' respectively."
    "Why there is no 'ts_moveZoffset' is because 'ts_moveZ' uses zoom. Plus, it already uses yoffset to adjust height."

    "Now for 'ts_moveinX(dist, ts_speed=0.5, start_pos=0-1200)-"
    "-and 'ts_moveinY(dist, ts_speed=0.5, start_pos=0-1200)"

    show oli at ts_moveinX(0.5)
    pause(1.5)
    show oli at ts_moveinY(1.0)
    pause(1.5)

    "Just like the name, ths transform moves the sprite from the 'start_pos' to 'dist'"
    "You may need to adjust the 'start_pos' depending on your sprite size."

    jump start

label tut_ts_rotations:
    camera at cam_reset
    show oli at center
    "Hoho you're in for a lot."
    "For most of the rotation transforms to work, have 'camera at reset' at the beginning of your label."
    "This resets the 'xrotation', 'yrotation', 'zrotation' to 0 and 'perspective' to 'True'. VERY important. (Sobs)"

    "For 'ts_rot(rot=15, ts_speed=0.3)', it doesn't need it as it rotates on the 2D space."
    "Let's rotate -90 and 90 degrees."
    show oli at ts_rot(-90)
    pause(1.0)
    show oli at ts_rot(0)
    pause(1.0)
    "Now for the rotations in 3D space."

    "First, 'ts_rotX(rot=15, ts_speed=0.3)'"
    "Rotating -90 degrees."
    show oli at ts_rotX(-90)
    pause(0.3)
    "Now rotating 90 degrees back."
    show oli at ts_rotX(0)
    pause(0.3)


    pause(0.3)
    "Now for 'ts_rotZ(rot=15, ts_speed=0.3)'"
    "Rotating 90 and -90 degrees."
    show oli at ts_rotZ(-90):
        xcenter 0.5
    pause(1.0)
    show oli at ts_rotZ(0):
        xcenter 0.5
    pause(0.3)
    camera at reset
    "All transforms for simple rotating start with 'ts_rot'"
    "For parameters: rot=rotation. Note that to return to original rotation you use {b}0{/b}."
    "For 'ts_rotZ', you must state the xcenter after every show statement for it to work properly."
    "You may have noticed that there is no 'ts_rotY'. That's becauze it's similar to 'ts_rot'."
    "If for some reason you want to add it in, it's the same as 'ts_rotX' and 'ts_rotZ'."
    "Just change the rotate to zrotate."

    "Next is 'ts_flipX(rot=1, ts_speed=0.0)' and 'ts_flipY(rot=1, ts_speed=0.0)'. These should be simple enough to understand."
    "Demonstrating now."

    show oli at ts_flipX(-1)
    pause(1.0)
    show oli at ts_flipX(1)
    pause(1.0)

    "ypos=0.5 to better demonstrate 'ts_flipY'"
    show oli:
        ease 0.5 ypos 540
    pause(1.5)
    show oli at ts_flipY(-1)
    pause(1.0)
    show oli at ts_flipY(1)
    pause(1.0)

    "Moving back"
    show oli:
        ease 0.5 ypos 1.0

    "The flips can also be executed using 'ts_rotZ' but it's easier to have a separate transform for them."
    "Note: use '1' (or dont, it's the default value) to flip/stay at default orientation, use '-1' to flip to other side."

    "Next is 'ts_tilt(xrot=0, yrot=0, ts_speed=0.3)' Like the name, this allows you to tilt using 'xrotation' and 'yrotation'"
    "Demonstrating with only 'xrot=20'"
    show oli at ts_tilt(xrot=20)
    pause(1.0)
    show oli at ts_tilt(0)
    pause(1.0)
    "Now for 'yrot=-20'"
    show oli at ts_tilt(0, -20)
    pause(1.0)
    show oli at ts_tilt(0, 0)
    pause(1.0)

    "Now for both 'xrot' and 'yrot'"
    show oli at ts_tilt(20, -20)
    pause(1.0)
    show oli at ts_tilt(20, 20)
    pause(1.0)
    show oli at ts_tilt(0, 0)
    pause(1.0)

    "Yeah! 'ts_tilt' can also be used with 'ts_acPanic' in \"Actions\" to create something reaaaal funny."
    "Like this."

    show oli at ts_tilt(20, 70), ts_acPanicX(config.screen_width+1000, ts_speed=2.0)
    "AAAAAH!"
    camera at cam_reset
    show oli:
        xoffset 0
    "Note: it is important for 'ts_tilt' to be first and then 'ts_acPanicX'."
    "Think of it like a child-parent relationship. Every transform affects the one before it."
    "Since 'ts_acPanicX' contains flipping, it needs to be after 'ts_tilt'"
    "Unless I'm wrong about the whole child-parent thing. IT just works this way for me lol."

    jump start

label tut_ts_actions:
    camera at cam_reset
    show oli at center
    "Action transforms are transforms for human actions: falling, jumping, shaking, etc."
    "All action transforms begin with 'ts_ac', In addition, most take rt(repeat X times) as a parameter. This is defaulted to None for infinity."
    "First falling. 'ts_acFall(ts_speed=0.2)"
    show oli at ts_acFall()
    "AAAAAAAAAAAAAAAAAAAAAAAAH!"
    show oli at center:
        yoffset 0

    "I'm back. 'ts_acFall' can be used with 'ts_moveZ'(in \"Moving XYZ\") for a funny effect!"
    "For demonstration."
    show oli at ts_moveZ(1.5)
    pause(0.5)
    show oli at ts_acFall()
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH!"

    show oli at center:
        yoffset 0
        zoom 1.0

    "Both transforms earlier use 'yoffset' to change Y pos of the character (not same as ypos). As a result, to bring back your character, be sure to reset their yoffset to 0."
    "Since 'ts_moveZ' uses 'zoom' be sure to reset that to '1.0'"
    "You could also make a transform for this but declaring it after show is easier for now."

    "Next, 'ts_acJump(dist, ts_speed=0.5)'-"
    "-and 'ts_acBounce(dist, ts_speed=0.5, pt=0.3, rt=None)'"
    "First, jump."
    show oli at ts_acJump(80)
    pause(1.0)
    "Next, bounce."
    show oli at ts_acBounce(80)
    "'ts_acBounce' is special in that you can customize the pause time (pt) between each bounce animation."

    show oli at center:
        yoffset 0

    "Next up is 'ts_acShake(dist, ts_speed=0.5, rt=None)'"
    show oli at ts_acShake(10, ts_speed=0.1)
    "This is exactly what I'm doing in this 30 degrees Farenheit weather."
    "This transforms handles both -/+ values so just put the distance for the shaking."

    show oli at center
    camera at cam_reset
    "So what comes after shake? SPINNING OF COURSE."
    show oli at ts_acSpin(1.2):
        xcenter 0.5
    "'ts_acSpin(ts_speed=0.5, xrot=0, yoff=0, rt=None)'"
    "This time, ts_speed is the first parameter primarily because I think people won't use 'xrot' and 'yoff' as much. What do they do?"
    show oli at ts_acSpin(5.0, xrot=50, yoff=50):
        xcenter 0.5

    "This probably looks a little familar to you if you've played {a=https://cuteshadow.itch.io/underholo}UnderHolo{/a} :)"

    camera at cam_reset
    show oli at center

    "Another thing you can do is..."
    camera at cam_reset
    show oli:
        offset (0, 0)
    show oli at ts_acSpin(5.0, yoff=-500), ts_rot(90, ts_speed=1.0):
        xcenter 0.5
    
    "Turn me into a rotisserie chicken..."
    "Yeah..."
    "This is using, in order, 'ts_acSpin' and 'ts_rot'"

    camera at cam_reset
    show oli at center

    "'yoff=yoffset' and 'xrot=xrotation' are on on the 3D plane."
    "For this transform, it's best to declare a 'camera' at the beginning of the label."
    "If you're only thinking of changing the spin speed, then don't worry about it."
    "Though I would still use if if you're using any of the 'ts_rot' transforms."

    "Next transforms are: 'ts_acPanicX(dist, ts_speed=0.5, rt=None)'"
    "-and 'ts_acFloat(dist, yoff=0, ts_speed=1.0, rot=0, rt=None)'"
    "For a demonstration..."
    show oli at ts_acPanicX(config.screen_width+1000, ts_speed=1.5)
    "THE SHIP IS SINKING! THE SHIP IS SINKING!"
    show oli at center:
        xoffset 0
        xzoom 1
    "As you can see, 'ts_acPanic' moves and flips the character from 'dist' to '-dist'"
    "These use 'xoffset' and 'xzoom' meaning...reset them!"
    "As for 'ts_acFloat'..."
    show oli at ts_acFloat(80)
    "The sprite will fall based on 'dist' and rise back up to the original position. If you don't want that, change 'yoff' to something other than 0."
    show oli at ts_acFloat(80, rot=5)
    "You can also add some rotation to it!"
    pause(1.0)
    show oli at center:
        offset (0, 0)
        rotate 0
    "That's all!"

    jump start
