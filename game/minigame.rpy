init python:
    herb_orders = [
        {"customer": "Mara", "herbs": ["Wormwood", "Ginseng"]},
        {"customer": "Iven", "herbs": ["Chrysanthemum", "Red Sage"]},
        {"customer": "Lio", "herbs": ["Turmeric", "Chrysanthemum"]},
        {"customer": "Sera", "herbs": ["Ginseng", "Wormwood"]},
        {"customer": "Tomas", "herbs": ["Turmeric", "Red Sage"], "crossed_out_name": "Nyima"},
    ]
    herb_supply = ["Wormwood", "Red Sage", "Turmeric", "Chrysanthemum", "Ginseng"]

    # Hitbox rectangles (x, y, w, h) for the herb supply art drawn in
    # images/minigame/minigame.png, left to right. The dragged name only
    # appears while one of these is being dragged.
    herb_slots = [
        (204, 16, 128, 152),   # Wormwood - green jar
        (392, 22, 128, 150),   # Red Sage - red jar
        (580, 104, 116, 58),   # Turmeric - yellow bowl
        (754, 108, 118, 58),   # Chrysanthemum - red bowl
        (910, 14, 130, 150),   # Ginseng - pale jar
    ]

    # Extra names shown in the label list. These are decoys.
    herb_decoy_labels = ["Nyima", "Odessa", "Perrin", "Sorrel", "Kael"]

    # The label list mixes the real customers with the decoys, shuffled once
    # so the decoys cannot be told apart by position. The order is fixed for
    # the whole playthrough.
    herb_label_order = [order["customer"] for order in herb_orders] + herb_decoy_labels
    renpy.random.shuffle(herb_label_order)

    def make_herb_jars():
        return [{"ingredients": [], "label": None, "sealed": False} for order in herb_orders]

    def order_for_label(label):
        for order in herb_orders:
            if order["customer"] == label:
                return order
        return None

    def label_is_assigned(label):
        return any(jar["label"] == label for jar in herb_jars)

    def jar_is_correct(jar_index):
        jar = herb_jars[jar_index]
        order = order_for_label(jar["label"])
        return bool(order) and sorted(jar["ingredients"]) == sorted(order["herbs"])

    def all_jars_sealed():
        return all(jar["sealed"] for jar in herb_jars)

    def herb_drag_started(drags):
        # Called when the mouse goes down on a herb drag. The matching name
        # text is drawn only while this is set, so the art stays clean at rest.
        global herb_dragging
        if not drags:
            return
        name = drags[0].drag_name
        if name.startswith("herb_"):
            herb_dragging = name[5:]
            renpy.restart_interaction()

    def herb_drag_clicked(drag):
        global herb_dragging
        herb_dragging = None
        renpy.restart_interaction()

    def herb_drag_hovered(herb):
        global herb_hovered
        herb_hovered = herb
        renpy.restart_interaction()

    def herb_drag_unhovered(herb):
        global herb_hovered
        if herb_hovered == herb:
            herb_hovered = None
        renpy.restart_interaction()

    def herb_dragged(drags, drop):
        global herb_dragging
        herb_dragging = None

        if not drags:
            return

        herb_drag = drags[0]
        dragged_name = herb_drag.drag_name
        if not dragged_name.startswith("herb_"):
            return

        # The draggable herb is a temporary copy layered over the fixed
        # supply card. It always returns to its source position after a drop.
        herb_drag.snap(herb_drag.start_x, herb_drag.start_y)

        if not drop or not drop.drag_name.startswith("jar_"):
            return

        jar_index = int(drop.drag_name[4:])
        jar = herb_jars[jar_index]
        herb = dragged_name[5:]

        if jar["sealed"]:
            renpy.notify("That jar is already sealed.")
        elif herb in jar["ingredients"]:
            renpy.notify("That jar already contains " + herb + ".")
        else:
            jar["ingredients"].append(herb)
            renpy.restart_interaction()

    def spawn_label(label):
        # Picking an available name closes the list and spawns a draggable copy.
        global herb_active_label, herb_labels_open, herb_label_spawn_serial
        if label_is_assigned(label):
            renpy.notify("That label is already on a jar.")
            return
        herb_active_label = label
        herb_label_spawn_serial += 1
        herb_labels_open = False
        renpy.restart_interaction()

    def label_dragged(drags, drop):
        global herb_active_label
        if not drags:
            return

        label = herb_active_label

        # The spawned label is consumed by any drop: it vanishes once it has
        # been placed on a jar, and is cancelled when dropped elsewhere.
        herb_active_label = None

        if not drop or not drop.drag_name.startswith("jar_"):
            renpy.restart_interaction()
            return

        jar_index = int(drop.drag_name[4:])
        jar = herb_jars[jar_index]

        if jar["sealed"]:
            renpy.notify("That jar is already sealed.")
        elif jar["label"]:
            renpy.notify("Remove this jar's current label first.")
        elif label_is_assigned(label):
            renpy.notify("That label is already on another jar.")
        else:
            jar["label"] = label
        renpy.restart_interaction()

    def show_jar_options(jar_index):
        global herb_selected_jar
        herb_selected_jar = jar_index
        renpy.show_screen("jar_options", jar_index=herb_selected_jar)
        renpy.restart_interaction()

    def jar_clicked(drag):
        show_jar_options(int(drag.drag_name[4:]))

    def jar_dragged(drags, drop):
        if not drags or not drop or drop.drag_name != "sealing_tray":
            return

        jar_drag = drags[0]
        jar_index = int(jar_drag.drag_name[4:])

        # The tray validates the jar, then returns it to its previous spot so
        # every prepared jar can use the same tray.
        jar_drag.snap(jar_drag.start_x, jar_drag.start_y)
        if jar_is_correct(jar_index):
            seal_jar(jar_index)
        else:
            renpy.notify("This jar does not match its labeled prescription yet.")

    def remove_jar_herb(jar_index, herb):
        jar = herb_jars[jar_index]
        if not jar["sealed"] and herb in jar["ingredients"]:
            jar["ingredients"].remove(herb)
            renpy.restart_interaction()

    def remove_jar_label(jar_index):
        jar = herb_jars[jar_index]
        if not jar["sealed"]:
            jar["label"] = None
            renpy.restart_interaction()

    def seal_jar(jar_index):
        if jar_is_correct(jar_index):
            herb_jars[jar_index]["sealed"] = True
            renpy.hide_screen("jar_options")
            renpy.restart_interaction()

    def reset_herb_minigame():
        global herb_jars, herb_prescription_open, herb_labels_open, herb_selected_jar, herb_active_label, herb_label_spawn_serial, herb_mislabeled_clue_found, herb_dragging, herb_hovered
        herb_jars = make_herb_jars()
        herb_prescription_open = False
        herb_labels_open = False
        herb_selected_jar = None
        herb_active_label = None
        herb_dragging = None
        herb_hovered = None
        # Keep the serial moving forward so a reset cannot reuse a drag position.
        herb_label_spawn_serial += 1
        herb_mislabeled_clue_found = False
        renpy.hide_screen("jar_options")
        renpy.restart_interaction()


default herb_jars = make_herb_jars()
default herb_prescription_open = False
default herb_labels_open = False
default herb_selected_jar = None
default herb_active_label = None
default herb_label_spawn_serial = 0
default herb_mislabeled_clue_found = False
default herb_dragging = None
default herb_hovered = None


# The large sheet from paper.png, cropped to its content and reused as the
# background for the jar options popup.
image packet_paper = Crop((346, 162, 586, 371), "images/minigame/paper.png")

# A single packet sprite from packet.png, cropped to its content. One is drawn
# per jar in the minigame.
image packet = Crop((6, 48, 239, 155), "images/minigame/packet.png")


# Every text displayable in the minigame screens uses the Baskerville face.
# The "herb" style prefix on the screens routes text through these styles.
style herb_text:
    font "gui/font/baskervville.regular.ttf"

style herb_button_text:
    font "gui/font/baskervville.regular.ttf"


screen herb_minigame():

    modal True
    style_prefix "herb"

    $ jar_positions = [(284, 204), (524, 202), (760, 204), (410, 386), (648, 380)]
    add "images/minigame/minigame.png"

    # The prescription book: the closed art is also the button, and the open
    # art provides the page the checklist is drawn onto.
    if herb_prescription_open:
        add "images/minigame/prescription_open.png"
    else:
        add "images/minigame/prescription_closed.png"

    imagebutton:
        idle Solid("#00000000")
        hover Solid("#00000000" if herb_prescription_open else "#ffffff12")
        xpos 0
        ypos 474
        xsize 318
        ysize 244
        action ToggleVariable("herb_prescription_open")

    if herb_prescription_open:
        vbox:
            xpos 70
            ypos 340
            xsize 288
            spacing 8

            text "Checklist" size 32 color "#3a2c1e" xalign 0.5 font "gui/font/Orange Lovely.otf"
            text "Prepare Customer Orders." size 20 color "#5c4a34" xalign 0.5 font "gui/font/Orange Lovely.otf"
            null height 8

            for prescription_index, prescription in enumerate(herb_orders):
                $ order_sealed = any(jar["sealed"] and jar["label"] == prescription["customer"] for jar in herb_jars)
                hbox:
                    spacing 4

                    if prescription_index == len(herb_orders) - 1:
                        textbutton "{s}[prescription['crossed_out_name']]{/s}":
                            action [SetVariable("herb_mislabeled_clue_found", True), Function(bobcachievement_grant, "mislabeled"), Notify("Clue Found: Mislabeled Name")]
                            text_size 24
                            text_font "gui/font/Orange Lovely.otf"
                            text_color "#080808"
                            text_hover_color "#c07a2a"
                            background None
                            padding (0, 0)

                    if order_sealed:
                        text "{s}[prescription['customer']] - [', '.join(prescription['herbs'])]{/s}" size 24 color "#6f7a68" yalign 0.5 font "gui/font/Orange Lovely.otf"
                    else:
                        text "[prescription['customer']] - [', '.join(prescription['herbs'])]" size 24 color "#241c16" yalign 0.5 font "gui/font/Orange Lovely.otf"



    # The label tab: closed art is the button, open art backs the name list.
    if herb_labels_open:
        add "images/minigame/label_open.png"

        imagebutton:
            idle Solid("#00000000")
            xpos 1054
            ypos 86
            xsize 224
            ysize 502
            action SetVariable("herb_labels_open", False)

        vbox:
            xpos 1075
            ypos 190
            xsize 200
            spacing 6

            # Real customer names plus decoys (shuffled once), shown as plain
            # selectable text.
            for label_name in herb_label_order:
                if label_is_assigned(label_name):
                    text "[label_name] (placed)":
                        xalign 0.5
                        size 24
                        color "#7a6a55"
                        font "gui/font/Orange Lovely.otf"
                else:
                    textbutton "[label_name]":
                        action Function(spawn_label, label_name)
                        xalign 0.5
                        text_size 24
                        text_font "gui/font/Orange Lovely.otf"
                        text_color "#241c16"
                        text_hover_color "#c07a2a"
                        background None
                        padding (0, 0)
    else:
        add "images/minigame/label_closed.png"

        imagebutton:
            idle Solid("#00000000")
            hover Solid("#ffffff12")
            xpos 1092
            ypos 160
            xsize 186
            ysize 78
            action SetVariable("herb_labels_open", True)

    draggroup:
        for herb_index, herb in enumerate(herb_supply):
            $ herb_slot_x, herb_slot_y, herb_slot_w, herb_slot_h = herb_slots[herb_index]
            drag:
                drag_name "herb_" + herb
                draggable True
                droppable False
                activated herb_drag_started
                clicked herb_drag_clicked
                dragged herb_dragged
                hovered Function(herb_drag_hovered, herb)
                unhovered Function(herb_drag_unhovered, herb)
                xpos herb_slot_x
                ypos herb_slot_y

                frame:
                    xysize (herb_slot_w, herb_slot_h)
                    background None
                    if herb_dragging == herb or herb_hovered == herb:
                        text "[herb]":
                            align (0.5, 0.5)
                            size 22
                            color "#fff3cf"
                            outlines [(2, "#3a2410cc", 0, 0)]

        
        if herb_active_label:
            drag:
                drag_name "active_label_" + str(herb_label_spawn_serial)
                draggable True
                droppable False
                dragged label_dragged
                xpos 1000
                ypos 230

                frame:
                    xysize (155, 43)
                    background "#d5b56f"
                    text "[herb_active_label]":
                        align (0.5, 0.5)
                        color "#241c16"
                        size 18

        for jar_index, jar in enumerate(herb_jars):
            $ jar_x, jar_y = jar_positions[jar_index]
            drag:
                drag_name "jar_" + str(jar_index)
                draggable not jar["sealed"]
                droppable not jar["sealed"]
                clicked jar_clicked
                dragged jar_dragged
                xpos jar_x
                ypos jar_y

                frame:
                    xysize (216, 140)
                    background Frame("packet", 0, 0)

                    vbox:
                        align (0.5, 0.5)
                        spacing 3
                        if jar["sealed"]:
                            text "[jar['label']]" size 15 color "#3f6b46" xalign 0.5
                        elif jar["label"]:
                            text "[jar['label']]" size 16 color "#241c16" xalign 0.5
                        else:
                            text "Unlabeled" size 14 color "#6a5138" xalign 0.5

                        if jar["ingredients"]:
                            for ingredient in jar["ingredients"]:
                                text "• [ingredient]" size 13 color "#241c16" xalign 0.5
                        else:
                            text "Empty" size 13 color "#6a5138" xalign 0.5

        drag:
            drag_name "sealing_tray"
            draggable False
            droppable True
            xpos 440
            ypos 548

            frame:
                xysize (430, 170)
                background None
                hover_background "#ffffff18"
                vbox:
                    align (0.5, 0.5)
                    spacing 1
                    text "SEALING TRAY" size 20 xalign 0.5 color "#fff3cf" outlines [(2, "#3a2410cc", 0, 0)]
                    text "Drop a correct packet here" size 13 xalign 0.5 color "#fff3cf" outlines [(2, "#3a2410cc", 0, 0)]

    if all_jars_sealed():
        timer 0.01 action Return(True)


screen jar_options(jar_index):

    modal True
    zorder 100
    style_prefix "herb"

    $ jar = herb_jars[jar_index]

    frame:
        xalign 0.5
        yalign 0.5
        xsize 586
        ysize 371
        background "packet_paper"

        vbox:
            align (0.5, 0.5)
            spacing 8
            text "Jar [jar_index + 1] options" size 24 color "#241c16" xalign 0.5
            if jar["sealed"]:
                text "This jar is sealed and cannot be changed." size 16 color "#4a3b2a" xalign 0.5
            else:
                if jar["ingredients"]:
                    text "Remove an ingredient/label:" size 16 color "#4a3b2a" xalign 0.5
                    for ingredient in jar["ingredients"]:
                        textbutton "Remove [ingredient]":
                            action Function(remove_jar_herb, jar_index, ingredient)
                            xalign 0.5
                            text_size 16
                            text_color "#3a2c1e"
                            text_hover_color "#8a5a2a"
                            background None
                else:
                    text "This jar has no herbs yet." size 16 color "#4a3b2a" xalign 0.5

                if jar["label"]:
                    textbutton "Remove [jar['label']] label":
                        action Function(remove_jar_label, jar_index)
                        xalign 0.5
                        text_size 16
                        text_color "#3a2c1e"
                        text_hover_color "#8a5a2a"
                        background None

            textbutton "Close":
                action Hide("jar_options")
                xalign 0.5
                text_size 17
                text_color "#3a2c1e"
                text_hover_color "#8a5a2a"
                background None
