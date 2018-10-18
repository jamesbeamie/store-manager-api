
[![Build Status](https://travis-ci.org/jamesbeamie/store-manager-api.svg?branch=ch-id-validation-161258357)](https://travis-ci.org/jamesbeamie/store-manager-api) [![Coverage Status](https://coveralls.io/repos/github/jamesbeamie/store-manager-api/badge.svg?branch=ch-feedback-test-161324174)](https://coveralls.io/github/jamesbeamie/store-manager-api?branch=ch-feedback-test-161324174)
## Store manager
- Store manager is an application for managing a boutique.The store deals in a wide range of clothes.
- The owner of the store is the primary admin with the rights to add new product to inventory, view all sales records, edit and delete an existing product.
- Store has attendants to serve the clients, who can search for products and add to cient's cart.
- The store owner can also add a new attendant and create their useraccounts.
## Testing locally
- The api can be locally tested by firts clonning the repository to your local machine.
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
## Versioning
- V1 is version one oof the application
## Author
- James Wafula
