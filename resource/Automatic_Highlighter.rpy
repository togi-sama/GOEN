#######################################################################################
#######################################################################################
#######################################################################################
############ Auto text coloring/highlighting for Ren'Py

# Hey there! Thanks for grabbing my little Ren'py tool.
# This tool automatically highlights/colors every character name in text a color of your choice.
# You can also optionally set a list of other words to be recolored.
#
# If you like this tool, consider checking out my games (Two and a Half Studios)!
#
#
# If you'd like to, you can credit "Gabmag", but it's not necessary :)
# - Gabmag


############## Set up ################################################################
# If you want to use the name auto highlighting, please paste "$ character_names = get_all_character_names()" (without quotes)
# after label start

# !!! IMPORTANT !!!
# If you update character names throughout your script after label start, you will need to call "$ character_names = get_all_character_names()" again.
# It's possible to do this automatically by updating character_names in highlight_text, but for large projects it can slow down your game, so it's better to do it manually.

############## Definitions ############################################################
define enable_character_name_highlighting = True  # Set to False to disable character name highlighting
define enable_word_highlighting = True  # Set to False to disable word highlighting

define highlight_words = {"Placeholder1", "Placeholder2"}  # Change/add words here to change their color
define highlight_color_words = "#ff0000"  # Change this color for highlighted words
define highlight_color_names = "#d85d26"  # Change this color for highlighted names

define persistent.character_names = set() # No need to touch this one, it automatically contains all character names

############## Function ##############################################################
init python:
    import re # imports the python module re so we can use regex

    def remove_renpy_tags(text): # Removes Ren'Py text tags from names (e.g., {sc}, {i}, {b}) so they highlight correctly if they're present.
        return re.sub(r"\{.*?\}", "", text)  # Removes anything inside curly braces {}


    def get_all_character_names(): # dynamically fetch all Character() instances and returns their names, then adds them to a list
        persistent.character_names.clear()  # Clear previous names
        for key, value in globals().items():
            if hasattr(value, "name") and isinstance(value.name, str):  # Check for valid character names
                cleaned_name = remove_renpy_tags(value.name)  # Strip {sc} or other tags
                persistent.character_names.add(cleaned_name) # Add the character name to the list
        return persistent.character_names

    def highlight_text(text): # Applies both character name highlighting and word highlighting, depending on if they are set to True

        # Step 1: Character Name Highlighting
        if enable_character_name_highlighting:
            escaped_names = [re.escape(name) for name in persistent.character_names]

            if escaped_names: # This section makes sure we match whole words only. E.g if you have a character called Bill, the 'Bill' in Billby won't highlight.
                pattern = r'\b(' + r'|'.join(escaped_names) + r')\b'
                text = re.sub(pattern, r"{{color={}}}\1{{/color}}".format(highlight_color_names), text)

        # Step 2: Word Highlighting
        if enable_word_highlighting:
            escaped_words = [re.escape(word) for word in highlight_words]

            if escaped_words:
                pattern = r'\b(' + r'|'.join(escaped_words) + r')\b'
                text = re.sub(pattern, r"{{color={}}}\1{{/color}}".format(highlight_color_words), text, flags=re.IGNORECASE)

        return text

############## Text Filter #############################################################
# Sets the text filter to use our new function, highlight_text.
# You may need to add 'highlight_text' to your existing filter if you already make use of it.

define config.say_menu_text_filter = highlight_text
