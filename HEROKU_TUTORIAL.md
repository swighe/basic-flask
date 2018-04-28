# Getting your Flask app onto the Internet via Heroku

Up until this point, you have been running your flask app on your home computer, with your computer acting as both the server (via the running Flask app) and the client (via a browser, or a tool on your terminal like curl or wget). In this state, no one except for you can access your app. Heroku is one of a number of companies that help to host your app on the internet, where anyone else connected to the network can access your app.

## Pre-Requisites
1. Ensure that your program works as intended when running locally.
2. Push your code to a repository on Github. You can use [Github Desktop](https://desktop.github.com/) for a simpler user interface.

## Files Required for Heroku

Create these files exactly as specified and add + commit + push them to your repo on Github.

1. Procfile
    * this text file named Procfile should be located at the same level as your python file
    * make sure that this does *NOT* have a file extension (~~Procfile.txt~~ BAD, Procfile GOOD)
    * the content of the file should be: `web: python <NAME_OF_YOUR_PYTHON_FILE>.py` with the correct name put in
    * [example](https://github.com/jameslinjl/basic-flask/blob/master/Procfile)
2. requirements.txt
    * this .txt file named requirements.txt should be located at the same level as your python file
    * the content of the file should be whatever python libraries you installed using `pip`
    * [example](https://github.com/jameslinjl/basic-flask/blob/master/requirements.txt)
    * if you are comfortable using the terminal, you can also run this command from the terminal (at the same level as your python file). You should run `pip freeze > requirements.txt` and this will generate a correct list for you.
3. runtime.txt
    * this .txt file named requirements.txt should be located at the same level as your python file
    * the content of the file should simply be `python-2.7.14` since we are using Python 2
    * [example](https://github.com/jameslinjl/basic-flask/blob/master/runtime.txt)
4. make changes to your python file
    * you will need to import os at the top of your file if you have not already
    * you need the following code in your flask python file where you start running the server:
```python
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)
```
5. Add + Commit + Push these files to your Github repo

## Heroku Setup

Now we just need to use the Heroku User Interface to link our Github repo with a new Heroku application.

1. Create a new, free [Heroku](https://www.heroku.com/) account (if you don't have one already).
2. Create a new Heroku app from the [Heroku Dashboard](https://dashboard.heroku.com). The name of your app will correspond to the URL at which it can be reached on the internet.
3. Go to the `Deploy` tab on your app dashboard.
4. Select `Github` for the `Deployment method` section.
5. Click `Deploy Branch` for `master` (assuming all of you are using `master` as your main branch) and your app should be working!
6. What if it isn't? Click `More` on the upper right and select `View logs`. This will show you logs from your app, which should point you in the right direction for debugging.
