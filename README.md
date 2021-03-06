
[![Build Status](https://travis-ci.org/jamesbeamie/store-manager-api.svg?branch=master)](https://travis-ci.org/jamesbeamie/store-manager-api) [![Coverage Status](https://coveralls.io/repos/github/jamesbeamie/store-manager-api/badge.svg?branch=develop)](https://coveralls.io/github/jamesbeamie/store-manager-api?branch=develop)
## Store manager - An online store to buy and sell clothings 
- Store manager is an application for managing a boutique.The store deals in a wide range of clothes.
- The owner of the store is the primary admin with the rights to add new product to inventory, view all sales records, edit and delete an existing product.
- Store has attendants to serve the clients, who can search for products and add to cient's cart.
- The store owner can also add a new attendant and create their useraccounts.
## Testing locally
- The api can be locally tested by first clonning the repository to your local machine.
- Create and activate your  virtual environment
- Run the application using _python run.py_ command
- Get the url and test it on postman using the relevant https request, including the right url prefix _/api/v1_

## Prerequisites
- You need to install Flask, a Server-side framework. _pip install Flask_
- PyTest, a python testing framework, _pip install PyTest_
## Running the tests
- On your loocal branch, navigate to the root folder and run _pytest -v_ for tests.
- To run tests with coverage, run _--cov=app/v1/_ to cover everything in v1 folder
## Deployment
- Deploy the api on heroku.
- Install gunicorn, and specify the application name in the procfile.
- Log into heroku using _heroku login_ command
- Create application on heroku
- Push changes from develop to heroku master
## Testing on heroku
- Get the heroku application link after deployment process above
- paste the link in the browser and add the url prefix and the route
- Copy the heroku link from the browser to postman
- Test the endpoints using the relevant requests
## Versioning
- V2 is version one of the application
## Author
- James Wafula
