init python:
    herb_orders = [
        {"customer": "Mara", "herbs": ["Moonmint", "Frost Sage"]},
        {"customer": "Iven", "herbs": ["Sunroot", "Red Clover"]},
        {"customer": "Lio", "herbs": ["Star Anise", "Moonmint"]},
        {"customer": "Sera", "herbs": ["Frost Sage", "Sunroot"]},
        {"customer": "Tomas", "herbs": ["Red Clover", "Star Anise"], "crossed_out_name": "Nyima"},
    ]
    herb_supply = ["Moonmint", "Sunroot", "Star Anise", "Frost Sage", "Red Clover"]

    # Extra names shown in the label list. These are decoys.
    herb_decoy_labels = ["Nyima", "Odessa", "Perrin", "Sorrel", "Kael"]

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

    def herb_dragged(drags, drop):
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
        # Picking a name from the list spawns a draggable copy of it.
        # The original entry stays in the list.
        global herb_active_label
        if label_is_assigned(label):
            renpy.notify("That label is already on a jar.")
            return
        herb_active_label = label
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
        global herb_jars, herb_prescription_open, herb_labels_open, herb_selected_jar, herb_active_label, herb_mislabeled_clue_found
        herb_jars = make_herb_jars()
        herb_prescription_open = False
        herb_labels_open = False
        herb_selected_jar = None
        herb_active_label = None
        herb_mislabeled_clue_found = False
        renpy.hide_screen("jar_options")
        renpy.restart_interaction()


default herb_jars = make_herb_jars()
default herb_prescription_open = False
default herb_labels_open = False
default herb_selected_jar = None
default herb_active_label = None
default herb_mislabeled_clue_found = False


screen herb_minigame():

    modal True

    $ jar_positions = [(410, 205), (570, 205), (730, 205), (490, 390), (650, 390)]
    add "room"

    textbutton "Prescription":
        action ToggleVariable("herb_prescription_open")
        xpos 25
        ypos 630

    if herb_prescription_open:
        frame:
            xpos 25
            ypos 390
            xsize 365
            ysize 230
            background "#2a222be8"

            vbox:
                align (0.5, 0.5)
                spacing 5
                xfill True
                text "Checklist" size 21 color "#f5d58a" xalign 0.5
                text "Match each label to its corresponding herb combination." size 13 color "#c7bdc8" xalign 0.5

                for prescription_index, prescription in enumerate(herb_orders):
                    $ order_sealed = any(jar["sealed"] and jar["label"] == prescription["customer"] for jar in herb_jars)
                    frame:
                        xsize 335
                        ysize 29
                        if order_sealed:
                            background "#426145"
                        else:
                            background "#473b4b"

                        hbox:
                            align (0.5, 0.5)
                            spacing 5
                            if order_sealed:
                                text "OK" size 13 color "#c9efaa"

                            if prescription_index == len(herb_orders) - 1:
                                textbutton "{s}[prescription['crossed_out_name']]{/s}":
                                    action [SetVariable("herb_mislabeled_clue_found", True), Notify("There’s a name crossed out messily in ink. Not a habit either of them have.")]
                                    text_size 15
                                    text_color "#d8a66d"
                                    text_hover_color "#fff0ae"
                                    background None
                                if order_sealed:
                                    text "{s}[prescription['customer']] - [', '.join(prescription['herbs'])]{/s}" size 14
                                else:
                                    text "[prescription['customer']] - [', '.join(prescription['herbs'])]" size 14
                            else:
                                if order_sealed:
                                    text "{s}[prescription['customer']] - [', '.join(prescription['herbs'])]{/s}" size 14
                                else:
                                    text "[prescription['customer']] - [', '.join(prescription['herbs'])]" size 14



    # Fixed supply cards remain in place while their draggable copies move.
    for herb_index, herb in enumerate(herb_supply):
        frame:
            xpos 178 + (herb_index * 187)
            ypos 100
            xysize (175, 46)
            background "#496044"
            text "[herb]":
                align (0.5, 0.5)
                size 18

    # The label list: names stay in place; clicking one spawns a draggable copy.
    textbutton "Labels":
        action ToggleVariable("herb_labels_open")
        xpos 1120
        ypos 172

    if herb_labels_open:
        frame:
            xpos 1060
            ypos 210
            xsize 210
            ysize 300
            background "#2a222be8"

            vbox:
                align (0.5, 0.5)
                spacing 6
                xfill True

                # Real customer names plus decoys, scrollable when the list
                # is taller than the panel.
                viewport:
                    xsize 186
                    ysize 205
                    mousewheel True
                    scrollbars "vertical"

                    vbox:
                        spacing 6
                        xfill True

                        $ label_list_names = [order["customer"] for order in herb_orders] + herb_decoy_labels
                        for label_name in label_list_names:
                            if label_is_assigned(label_name):
                                frame:
                                    xsize 180
                                    ysize 34
                                    background "#3c3540"
                                    text "[label_name] (placed)":
                                        align (0.5, 0.5)
                                        size 15
                                        color "#8f8494"
                            else:
                                textbutton "[label_name]":
                                    action Function(spawn_label, label_name)
                                    xalign 0.5
                                    xsize 180
                                    text_size 16
                                    text_color "#241c16"
                                    text_hover_color "#fff0ae"
                                    background "#d5b56f"
                                    hover_background "#e8ca86"

    draggroup:
        for herb_index, herb in enumerate(herb_supply):
            drag:
                drag_name "herb_" + herb
                draggable True
                droppable False
                dragged herb_dragged
                xpos 178 + (herb_index * 187)
                ypos 100

                frame:
                    xysize (175, 46)
                    background "#496044"
                    text "[herb]":
                        align (0.5, 0.5)
                        size 18

        # The spawned label copy. It appears next to the list when a name is
        # picked, and vanishes once it has been dropped.
        if herb_active_label:
            drag:
                drag_name "active_label"
                draggable True
                droppable False
                dragged label_dragged
                xpos 890
                ypos 215

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
                    xysize (135, 145)
                    if jar["sealed"]:
                        background "#4c7351"
                    elif jar["label"] and jar_is_correct(jar_index):
                        background "#768f5a"
                    else:
                        background "#9b7653"

                    vbox:
                        align (0.5, 0.5)
                        spacing 5
                        text "JAR [jar_index + 1]" size 18 xalign 0.5
                        if jar["sealed"]:
                            text "SEALED" size 16 color "#f5d58a" xalign 0.5
                        elif jar["label"]:
                            text "[jar['label']]" size 17 color "#241c16" xalign 0.5
                        else:
                            text "Unlabeled" size 15 xalign 0.5

                        if jar["ingredients"]:
                            for ingredient in jar["ingredients"]:
                                text "• [ingredient]" size 14 xalign 0.5
                        else:
                            text "Empty" size 14 xalign 0.5

                        if not jar["sealed"] and jar["label"]:
                            if jar_is_correct(jar_index):
                                text "Ready for tray" size 13 color "#d9f2ab" xalign 0.5
                            else:
                                text "Recipe incomplete" size 12 color "#ffd4d4" xalign 0.5

        drag:
            drag_name "sealing_tray"
            draggable False
            droppable True
            xpos 510
            ypos 565

            frame:
                xysize (260, 58)
                background "#5f4b39"
                vbox:
                    align (0.5, 0.5)
                    spacing 1
                    text "SEALING TRAY" size 20 xalign 0.5
                    text "Drop a correct jar here" size 13 xalign 0.5

    if all_jars_sealed():
        timer 0.01 action Return(True)


screen jar_options(jar_index):

    modal True
    zorder 100

    $ jar = herb_jars[jar_index]

    frame:
        xalign 0.5
        yalign 0.5
        xsize 440
        ysize 330
        background "#332b35f2"

        vbox:
            align (0.5, 0.5)
            spacing 12
            text "Jar [jar_index + 1] options" size 28 xalign 0.5
            if jar["sealed"]:
                text "This jar is sealed and cannot be changed." size 19 xalign 0.5
            else:
                if jar["ingredients"]:
                    text "Remove an ingredient:" size 19 xalign 0.5
                    for ingredient in jar["ingredients"]:
                        textbutton "Remove [ingredient]":
                            action Function(remove_jar_herb, jar_index, ingredient)
                            xalign 0.5
                else:
                    text "This jar has no herbs yet." size 19 xalign 0.5

                if jar["label"]:
                    textbutton "Remove [jar['label']] label":
                        action Function(remove_jar_label, jar_index)
                        xalign 0.5

            textbutton "Close":
                action Hide("jar_options")
                xalign 0.5