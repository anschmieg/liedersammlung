def chordpro_to_latex(input):
    """
    Convert ChordPro to LaTeX
    @param input: ChordPro string to convert (usually file content)
    @return: LaTeX string with the converted content
    """

    # Initialize LaTeX output
    song_meta = {}
    output = ""

    # Define ChordPro directives and their LaTeX equivalents
    latex = {
        "env": "song",
        "chord_marker": "guitarChord",   
    }
    
    meta_directives = {
        "title": "title",
        "subtitle": "subtitle",
        "artist": "composer",
        "lyrics": "lyrics",
        "key": "key",
        "capo": "capo",
        "lyricist": "lyrics",
        "arranger": "composer",
        "composer": "composer",
        # "tempo": "tempo",
        # "time": "tempo",
    }
    directives = {
        "comment": "",
        "start_of_chorus": "",
        "end_of_chorus": "",
        "start_of_verse": "",
        "end_of_verse": "",
        "start_of_bridge": "",
        "end_of_bridge": "",
        "soc": "",
        "eoc": "",
        "sov": "",
        "eov": "",
        "sob": "",
        "eob": "",
        "new_page": "",
        "np": "",
    }

    def fallback(exp):
        nonlocal output
        output += exp + "\n"
        raise UserWarning(
            "Undefined sequence: "
            + exp
            + "\nCheck if this argument is supported. Writing original line to output."
        )

    def handle_directive(directive, content=None):
        nonlocal output
        nonlocal song_meta

        # if directive is a song property, store it in the dictionary
        if content and directive in meta_directives:
            song_meta[directive] = content
        # if directive is valid and has content, add it as an argument
        elif content and directive in directives:
            output += "\\" + directives[directive] + "{" + content + "}\n"
        # otherwise just add the directive
        elif directive in directives:
            output += "\\" + directives[directive] + "\n"
        # if directive is unknown, add it as plain text
        else:
            output += directive + ":" + (content if content else "") + "\n"
            return False  # return False to indicate that the directive is unknown

        return True
    
    def handle_line(line):
        nonlocal output
        # Change [test] to \Ch{test}
        line = line.replace("[", "\\" + latex["chord_marker"] + "{").replace("]", "}")
        output += line + "\n"
        return True

    input = input.strip()
    lines = input.split("\n")

    # Process each line
    for line in lines:
        line = line.strip(" \t")  # strip spaces, tabs and {}
        if "{" in line:
            line = line.strip("{} ")
            if ":" in line:
                # Split directive and content by ': ' or ':'
                directive, content = (
                    line.split(": ", 1) if ": " in line else line.split(":", 1)
                )
                handle_directive(directive, content)
            else:
                try:
                    # Use standalone directive
                    handle_directive(line)
                except:
                    fallback(line)
        else:
            try:
                handle_line(line)
            except:
                fallback(line)

    # Extract the title from the song metadata
    title = song_meta.pop('title')

    # output the song metadata as arguments to the \begin command
    output = "\\begin{" + latex["env"] + "}{" + title + "}{" + ", ".join(f"{arg}={{{song_meta[arg]}}}" for arg in song_meta) + "}\n" + output + "\\end{" + latex["env"] + "}"
    return output

