# %%
def chordpro_to_latex(input):
    # Initialize LaTeX output
    song_meta = "\\beginsong{\n"
    output = ""

    # Define ChordPro directives and their Leadsheet equivalents
    meta_directives = {
        "title": "title",
        "artist": "artist",
        "subtitle": "subtitle",
        "arranger": "composer",
        "composer": "composer",
        "lyricist": "lyrics",
        "lyrics": "lyrics",
        "key": "key",
        "tempo": "tempo",
        "time": "tempo",
        "capo": "capo",
    }
    directives = {
        "title": "title",
        "artist": "artist",
        "subtitle": "subtitle",
        "comment": "comment",
        "start_of_chorus": "chorus",
        "end_of_chorus": "endchorus",
        "start_of_tab": "tab",
        "end_of_tab": "endtab",
        "start_of_verse": "verse",
        "end_of_verse": "endverse",
        "start_of_bridge": "bridge",
        "end_of_bridge": "endbridge",
        "start_of_grid": "grid",
        "end_of_grid": "endgrid",
    }

    def fallback(line):
        nonlocal output
        output += line + "\n"
        raise UserWarning(
            "Undefined sequence: "
            + line
            + "\nCheck if this argument is supported. Writing original line to output."
        )

    def handle_directive(directive, content=None):
        nonlocal output, song_meta
        # if directive is a song property, prepend it
        if content and directive in meta_directives:
            song_meta += directives[directive] + "={" + content + "}\n"
        # if directive is valid and has content, add it as an argument
        elif content and directive in directives:
            output += "\\" + directives[directive] + "{" + content + "}\n"
        # otherwise just add the directive
        else:
            output += "\\" + directives[directive] + "\n"
        return True

    def handle_line(line):
        nonlocal output
        # Change [test] to \chord{test}
        line = line.replace("[", "\\writechord{").replace("]", "}")
        output += line + "\n"
        return True

    input = input.strip()
    lines = input.split("\n")

    # Process each line
    for line in lines:
        if line.startswith("{"):
            if ":" in line:
                try:
                    # Split directive and content by ': ' or ':'
                    directive, content = (
                        line.strip("{} ").split(": ", 1)
                        if ": " in line
                        else line.strip("{} ").split(":", 1)
                    )
                    handle_directive(directive, content)
                except:
                    fallback(line)
            else:
                try:
                    # Use standalone directive
                    directive = line.strip("{}")
                    handle_directive(directive)
                except:
                    fallback(line)
        else:
            try:
                handle_line(line)
            except:
                fallback(line)

    # Return the LaTeX result
    output = song_meta + "}\n" + output
    return output


# %%
# Try with songs/sonne.cho
with open("songs/sonne.cho", "r") as file:
    input = file.read()
    output = chordpro_to_latex(input)
    print(output)

# %%
