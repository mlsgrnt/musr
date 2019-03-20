# MUSR

MUSR is a Django web application where users can share songs they care about, and see what others are sharing.

## Lab group 4 - Team B
- Miles Grant 2386227
- Scott Isaac	2419523
- Callum Hunter	2247415

The source code is available at [https://github.com/mlsgrnt/musr](https://musr.pythonanywhere.com) and is deployed at [https://musr.pythonanywhere.com](https://musr.pythonanywhere.com).

## To deploy locally:
This project runs on Python 3.

To clone the repository, run

`git clone https://github.com/mlsgrnt/musr`

Once the repository is locally cloned, enter the installation directory:

`cd musr`

Next, install the dependencies with

`pip install -r requirements.txt`

If the database is empty, some errors will appear. To fix this, run the migrations, and run the population script:

```
python musr_project/manage.py migrate
python musr_project/populate_musr.py
```

Start a test server by running

`python musr_project/manage.py runserver`

Please note that while debug mode is active on the settings.py shipped in this repository, it has been turned off on the PythonAnywhere instance

#### Important notice:
Some features will not be functional when running the application on localhost, namely
###### 1) OAuth based authentication, more specifically the Facebook and Google logins
###### 2) The add post functionality

The reason for both of these is rooted in security. Storing secret client keys in plaintext is very bad practice, and so these keys are stored in the Django database. The population script inserts dummy keys which will not work in practice. We can provide working keys, as well as instructions on how to insert them into the database, through a secure channel. Otherwise, the login works on the deployed version of the application. The add post functionality, too, is disabled out of security concerns. The server which returns the search results is [CORS enabled](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), as is standard in modern web applications. To prevent malicious misuse of the proxy server, the [Access-Control-Allow-Origin header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) has been set to `https://musr.pythonanywhere.com`. Requests coming from any other host will not be accepted. To get the add-post functionality when running from localhost, a new proxy server has to be set up. See the source code of the proxy server for details. Then, either modify `add-post.js` line 83 to point to the new server, or redirect locally in your system’s hosts file.
## External Resources:
### Tooling:
##### [Black](https://github.com/ambv/black)
Python auto-formatter to ensure code consistency.
##### [pre-commit](https://github.com/chriskuehl/pre-commit)
Prevents any contributor from committing code that hasn’t been formatted by black.
##### [CodeCov](https://codecov.io)
Monitors the test coverage of every pull request.
##### [Travis CI](https://travis-ci.com)
Prevents the merging of a pull request which does not pass all test cases.
### Libraries and Dependencies:
##### [django-allauth](https://github.com/pennersr/django-allauth)
Used to implement OAuth authentication, forgot password mechanism, email confirmation mechanism.
##### [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)
Used to customize the django-allauth forms.
##### [poco.css framework](https://github.com/hihayk/poco)
This “minimal set of CSS variables and utilities” provides a set of base variables and classes which allow for writing clean CSS.
##### [focus.css framework](https://hihayk.github.io/focus/)
This “framework” contains a few extra css rules for common components such as buttons and input fields which build upon poco.css.
##### [lodash](https://lodash.com)
Only the denounce method of lodash is imported. It is used to fire requests in a reasonable manner in the add post interface.
##### [avataaars](https://getavataaars.com/?avatarStyle=Transparent&clotheType=BlazerShirt&facialHairType=Blank&skinColor=Yellow&topType=LongHairShavedSides)
Default profile picture sourced from the excellent Avataaars collection.

### External APIs
##### [Deezer song search API](https://developers.deezer.com/api)
Used to provide song search, info, and song previews.

## Deezer API CORS Proxy server
The Deezer API can not be called directly from the browser due to CORS restrictions. To overcome this, a CORS proxy has been set up which restricts API calls to coming from the MUSR website. This enables the client-side Ajax-enabled song search. The source code for this server is available here:
<!-- View Source Button --><a href="https://glitch.com/edit/#!/deezer-proxy">  <img src="https://cdn.glitch.com/2bdfb3f8-05ef-4035-a06e-2043962a3a13%2Fview-source%402x.png?1513093958802" alt="view source button" aria-label="view source" height="33"></a>

This server makes use of [ZEIT’s micro framework](https://zeit.co/blog/micro-8), as well as the [micro-cors](https://github.com/possibilities/micro-cors) package from NPM. These are used to create an extremely simple CORS-enabled proxy server.
