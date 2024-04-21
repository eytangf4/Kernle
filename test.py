pageContent = "hi"
prompt = ("summarize this wikipedia article in extremely easy to read "
        "and very simple language that highlights the intuition and main idea "
        "of the concept as opposed to focusing on the specific details. "
        "make this summary a very short 30 second read (max 100 words) and "
        "broken into 2-3 paragraphs of 1-2 sentences where each paragraph "
        "covers a different piece of the intuition. place that piece as a "
        "bolded title before each paragraph. Make sure the paragraphs do not "
        "repeat themselves. make it more simple:\n\n\n"
        + pageContent)

print(prompt)