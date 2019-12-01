DESCRIPTION
===========

Domicilian is an app that helps people make informed decisions while finding a home from the daunting task of renting/purchasing homes.

It is always a daunting task to search for a new place to rent or buy. Budget and commute restrictions further make it cumbersome to find such places.
We want to help users find desirable places faster and more efficiently using interactive visualization techniques, which can also help them see nearby amenities. We plan to highlight places where investments are worthwhile according to trends in the market prices to help users make informed decisions.

We've several different visualizations available and live demo hosted at:
https://domicilian.sanyamkhurana.com/

DIRECTORY STRUCTURE
============================

Reference from root of the `CODE` repository.

/scripts  -- just for reference

    *.py files contains scripts for parsing/loading data in DB.
    *.ipynb contains all experiments related to ML algorithm exploration and finally using Random Forest for prediction and loading data in the database.

/provisioner

    Contains ansible script to setup a server and host the application.

/tests

    Contains tests for the application.

/docs

    Contains docs related to API and application in general.

/domicilian

    The main folder for Django. Contains different django apps. This is where our backend rest endpoints and frontend code is there

/domicilian/static

    Contains all static css and js files

/domicilian/templates

    Frontend html files

/domicilian/visualization and /domicilian/median_prices

   Backend rest endpoints

/domicilian/urls.py

  URL mappings

If you have processed the dataset in some ways, include the code you used, and the steps people will need to go through.

  - Our code to process the datasets are in the scripts directory. Some of the csv files contained comma within the content (mainly neighborhood information), In order to process that we had to write a custom method that splits the data and not use the normal split command.
  - Users would not need to run these scripts because we have already provided our postgres dump file to load the data on one's local machine. Please see "INSTALLATION INSTRUCTIONS AND EXECUTION" below.
  - Please do not run these scripts. This is just for information purposes since I removed the data directory in each of the directories in these scripts to reduce our canvas submission size.
  - Link to raw data https://drive.google.com/file/d/1I0OL6fubD13JIGc-V_AEmKLPalYyu7_8/view?usp=sharing


INSTALLATION INSTRUCTIONS AND EXECUTION
=======================================

Before running the following instructions, make sure you get the following dependencies for your system. These packages installation differ from system to system and we've tested our setup locally on macOS and deployed on an Ubuntu 18.04 LTS AWS EC2 instance at https://domicilian.sanyamkhurana.com/

- gdal
        - For macOS:
	    - brew update
            - brew install gdal --HEAD
        - For Ubuntu:
            sudo add-apt-repository -y ppa:ubuntugis/ppa
            sudo apt update
            sudo apt upgrade
            sudo apt install gdal-bin python-gdal python3-gdal

- PostgreSQL 11 with postgies 2.4
        - For macOS refer: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac
        - For Ubuntu:
            sudo apt update
            sudo apt install postgresql postgresql-contrib


- Ensure a valid version of Py3.x (where 6 <= x <= 7) installed. We've tested this on Python 3.6 and Python 3.7
  Run the following command "brew install python3"

- Ensure a python3-pip installed on your system.

- Ensure the following packages for Ubuntu based system:

      - libjpeg-dev
      - libtiff5-dev
      - zlib1g-dev
      - libfreetype6-dev
      - liblcms2-dev
      - postgresql-client
      - libpq-dev

__NOTE__: Run the subsequent commands from the root of the repository containing the source code:

- Setup virtualenv with:

    virtualenv -p python3 venv

- Activate virtualenv with:

    source venv/bin/activate

- Add dependencies for project:

    pip install -r requirements/development.txt
    or pip3 install -r requirements/development.txt depending on the python version your system is on.
    brew install gdal
    pip install python-magic-bin==0.4.14 or pip3 install python-magic-bin==0.4.14 depending on your python version

- Upgrade priviliges to postgres user by

    sudo su postgres

- Login to psql shell to run commands related to postgres

    psql

- Create user cse6242 with password cse6242 by the following postgres command

    CREATE USER cse6242 WITH PASSWORD 'cse6242';

- Create database named `housing_data` in Postgres:

    CREATE DATABASE housing_data;

- Grant this user privileges by running the following command

    GRANT ALL PRIVILEGES ON DATABASE housing_data TO cse6242;

- Give user SUPERUSER priviliges

    ALTER USER cse6242 WITH SUPERUSER;

- Check out the dump of the database from URL:
  https://drive.google.com/file/d/1yK27L6rLrjOK3BdkgOuzXH3Go87shuoa/view?usp=sharing

- Unzip & Restore the Dump using the following command:

    unzip housing_data_final_pg_dump.zip
    psql housing_data < housing_data_final.bak


- Exit the psql CLI as well as the user postgres by pressing Ctrl + D twice.


- Ensure that you're now on CLI with your main user with venv activated like:

    (venv) /home/ubuntu/DVA_Final_Project $

- Rename or copy `.env.sample` to `.env`. This file contains all secrets so that they are not in source code and provided separately to all hosted instances including local setup. This strictly follows the 12-factor app style (https://12factor.net/). For demo purposes, it contains fake information so that the demo can be run.

    cp .env.sample .env

- Run the development server with:

    python manage.py runserver

We've excluded step to run django migrations, since they are part of the dump that is provided.

The site is now served at localhost:8000


OPTIONAL: In order to run tests for the app, run command `pytest` from root of the repo.

__NOTE__: Since system dependencies (differing based on an operating system like PostgreSQL, gdal, etc.) are hard to set up and control, we realize that it might happen that system dependencies are conflicted causing local setup to fail sometimes and hard to debug. Although we intend to be as clear as possible, and despite testing these instructions several times, we have set up a fallback method in case things don't work as expected.

We've also provided an optional but useful live demo of the code on https://domicilian.sanyamkhurana.com/

Although, we would've loved to package this app as a docker image to be easily utilized across the system, unfortunately, we were restricted by time constraints, but we've tried our best to set up Fabric and Ansible script for deployment on server available under `provisioner` folder. More info is in README.md file at the root of the repo.

