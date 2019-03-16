# MUSR

MUSR is a Django web application where users can share songs they care about, and see what others are sharing.

## External Resources:
### Tooling:
- Black
- pre-commit
- CodeCov
- Travis CI
### Imported software:
- Django allauth plugin
- django-widget-tweak
- poco.css css framework
- focus.css css rules
- lodash

### Code hosted elsewhere:
The Deezer API can not be called directly from the browser due to CORS restrictions. To overcome this, a CORS proxy has been set up which restricts API calls to coming from the MUSR website. This enables the client-side Ajax-enabled song search. The source code for this server is available here:
<!-- View Source Button --><a href="https://glitch.com/edit/#!/deezer-proxy">  <img src="https://cdn.glitch.com/2bdfb3f8-05ef-4035-a06e-2043962a3a13%2Fview-source%402x.png?1513093958802" alt="view source button" aria-label="view source" height="33"></a>
