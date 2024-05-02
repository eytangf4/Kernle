import wikipedia
from openai import OpenAI
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()

def userSearchToTopPage (userSearch):
    topArticle = wikipedia.search(userSearch, 1)
    return topArticle[0]

def pageToText (concept):
    wikiPage = wikipedia.WikipediaPage(title=concept)
    # using wikipedia.WikipediaPage as opposed to wikipedia.page since WikipediaPage
    # also contains data from a Wikipedia page but also uses property methods to filter data from the raw HTML.
    # this helps chatGPT to understand the page better
    # (I know this because I tried using both 'page' and 'WikipediaPage' and 'WikipediaPage' gave me clearer kernel summaries
    return wikiPage.content

def createPrompt (pageContent):
    prompt = ("summarize this wikipedia article delimited by quotes in extremely easy to read "
            "and very simple language that highlights the intuition and main idea "
            "of the concept as opposed to focusing on the specific details. "
            "make this summary a very short 30 second read (max 100 words) and "
            "broken into 2-3 paragraphs of 1-2 sentences where each paragraph "
            "covers a different piece of the intuition. place that piece as a "
            "bolded title before each paragraph. Make sure the paragraphs do not "
            "repeat themselves. do not use words from the article in the summary, make the summary readable for a kindergartener. make it more simple: \n\n\n"
            + "\"" + pageContent + "\"")
    return prompt

def promptToAIResponse (prompt):


    client = OpenAI(api_key = os.getenv("my_api_key"))

    response = client.chat.completions.create(
        messages=[{"role": "assistant", "content": prompt,}],
        model="gpt-3.5-turbo",
    )

    return response

def userSearchToAIResponse(userSearch):
    topPage = userSearchToTopPage(userSearch)
    pageText = pageToText(topPage)
    prompt = createPrompt(pageText)
    response = promptToAIResponse(prompt)
    return response.choices[0].message.content

# creates an instance of a flask web application
app = Flask(__name__)

# decorates the 'home' function to let the app know when the url has [domain name]/, the app calls 'home'
# methods tells flask which methods this function is allowed to use, every method in the html file a func is 
# trying to render must be allowed here

@app.route("/", methods = ["get","post"])
# each 'def' defines a page that will be on the website
def home():
    return render_template("index.html")


@app.route("/summary", methods = ["get","post"])
def summary():
    userInput = request.form.get("fconcept")
    try:
        AIoutput = userSearchToAIResponse(userInput)
        return render_template("summary.html", content=AIoutput)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        return render_template("ambiguous.html", options=options, concept=userInput)

@app.route("/ambiguous", methods = ["get","post"])
def resolve_ambiguity():
    # need "if-else" so that error is not thrown if user types in "/ambiguous" at the end of the url.
    # the redirect to summary only runs if an ambiguous redirect came from a disambiguation error,
    # otherwise it just redirects to home
    if request.method == "get":
        return redirect(url_for("summary"))
    else:
        return redirect(url_for("home"))

@app.route("/about", methods = ["get","post"])
def about():
    return render_template("about.html")

#runs the app
if __name__ == "__main__":
    app.run(debug=True)