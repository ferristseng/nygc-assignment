## Note!

In an attempt to make this small enough to send via. email, I deleted the data files. You'll have to add them
back to run this code.

# Windy City Crime

This repository houses the coding assignments used by NYGC SWENG to evaluate interview candidates on their
technical engineering skills. Each assignment touches on specific topics to allow candidates to demonstrate
proficiencies in the various technologies we use at NYGC. As a candidate, you may be asked to execute on one
or more of these assignments, varying based on the position being applied for.

In general, you should tackle these exercises as you would any problem you encounter in your normal day to day.
That means you should feel free to search for and use any online references you can find to assist you in creating
the best solution you can in the time you have. You will not be evaluated on just the correctness of your
solutions. We also highly value your ability to explain your thought process and justify the choices you made to
arrive that those solutions.

Good luck!

## Prerequisites

**First**, we will be using a Google Cloud Platform provided dataset to drive the work in these assignments.
For convenience, we have included a compressed CSV file of the dataset for you to work against and you should
unzip this file locally.

```sh
gunzip -c data/crime.csv.gz > data/crime.csv
```

**Next**, if you do not have a Python development environment readily available, we have provided the docker 
compose file and configuration files to support remote container development in Visual Studio Code. For more details,
check out the [documentation](https://code.visualstudio.com/docs/remote/containers#_getting-started). Once you have 
installed the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
extension, you can run the `Remote-Containers: Open Folder in Container` command in VSCode and target the root of this
repository to launch into a remote container session in the Python docker container we have provided for you.

Alternatively, you can go ahead and do all the Python development work in a development environment on your host machine,
if you are set up to do so.


# Assignment 1 - ETL in Python

This assignment will review your basic proficiency in Python by having you perform an ETL operation on a 
fixed CSV dataset. The ETL process should be run with the following command:

```bash
$ python -m scripts.run_etl
```

Success criteria:
- Running the python script should successfully execute the parsing logic and export the data
    from the CSV into the requested format.
- All the test assertions pass on the resulting dataset.


Be prepared to:
- Walk us through the details of your solution and point out any specific optimizations made.
- Discuss any further optimizations that could be made, given more time and thought.

View the assignment details [here](./scripts/run_etl.py).


# Assignment 2 - ETL to SQL Database

This assignment gives you an opportunity to demonstrate your proficiency with data modeling and database scripting.

**First**, using the same dataset as [Assignment 1](#assignment-1---etl-in-python), design a database schema to best 
represent the data in the [CSV file](./data/crime.csv) in order to support queries to answer the following questions. 
Assume that we will want to build a reporting application that will run queries for these answers on a frequent basis:

- What is the list of all the types of committed crimes (primary_type) in the dataset?
- For any given year, what type of crime (primary_type) was the most frequently committed?
- What percentage of each type of crime (primary_type) ended in arrest (arrest == true)?
- What is the frequency of each crime type (primary_type) year over year? Imagine we want to generate datapoints
    to graph the number of occurrences of each crime type over every year in the dataset.
- For any beat, district, ward or community (only one will be provided at a time), retrieve all the unique keys
    of each crime incident ordered by date.

**Next**, using any preferred tools, script the creation of the proposed data schema and the import of the data into a
Postgres database. For convenience, we have provided a docker-compose file for a simple Postgres database that can
be started as follows:

```bash
$ docker compose up db
```

The credentials can be found in the `.env` file at the root of this project.

Once started, you should have an empty database available at: `jdbc:postgresql://localhost:5432/interview_db`. We are using
a docker volume so the data should persist between container and host restarts. Feel free to create the schema and import
the data using any database frameworks and tools you are familiar with.

**Finally**, construct some sample queries that you would use to answer some of the questions listed above. Just tackle the
ones you feel comfortable on and feel free to adjust the data model as you work through the problem. Consider how you would go
about optimizing those queries to be run on a continuous basis by several users on a daily basis. Consider what database 
constructs and features you would use to reduce stress on the SQL server and improve query responsiveness, given the nature 
of the dataset. These sample queries do not have to be exhaustive and are meant to drive the in-person conversation during
the review session.


# Assignment 3 - Working with APIs

 This assignment is intended to test your ability to implement features in the Flask web framework while integrating
 with a Postgres database.

**First**, start the docker container with the provided Postgres database.
```sh
$ docker compose up db
```

Upon container startup, this database will automatically be populated with a `interview_db.covid_state_stats` table.
You should connect to the database to make sure the table is there and has data. The database credentials should be
available in the `.env` file.

**Next**, install the project's dependencies, then run the flask application:

```sh
$ python -m api

# Use provided endpoint to verify that flask is able to establish a tcp connection with the database.
$ curl http://localhost:5001/covid-stats/test-db-connection

# If debugging the api in docker, add the host=host.docker.internal to the url.
$ curl http://localhost:5001/covid-stats/test-db-connection?host=host.docker.internal
```

**Finally**, create two api endpoints: one to serve records from the `covid_state_stats` table, and one to persist
changes to existing records from `covid_state_stats`. A single endpoint that accepts multiple request methods is
acceptable. The database credentials can be found by looking up the environment variables that were injected into flask
from `.env`.

```python
# use host.docker.internal instead of localhost if debugging the api in docker
# host = "host.docker.internal"
host = localhost
port = 5432
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db = os.environ["POSTGRES_DB"]
```

Success criteria:
- Serving records from the `covid_state_stats` table
    - Records are served in json format.
    - Datetime fields are in the ISO 8601 format.
    - Results are paginated.
- Persisting records to the `covid_state_stats` table
    - Can persist changes to an existing record.
    - All fields except for primary key should be settable to values allowable by their respective data type in the
    `covid_state_stats` table.

# Assignment 4 - Working with React

This assignment builds upon [Assignment 3](#assignment-3---working-with-apis) and is intended to test your proficiency
in implementing features in React based applications. If necessary, the api endpoint may be updated to support features
from this assignment.

**First**, navigate to the `ui` directory, install the project's dependencies, then run the development server with the
below command.

```sh
$ cd ui
$ npm install
$ npm start
```

**Next**, implement a page displaying information from the api endpoint in [Assignment 3](#assignment-3---working-with-apis).
This page does not have to be aesthetically pleasing, but it should have good usability. The data on this page should 
be modifiable as well using the api endpoint from the previous assignment. Though not required, feel free to use any
third party tools or libraries to help complete the assignment.

Success criteria
- Viewing data
    - The covid data table is paginated. Users may navigate to the `next` or `previous` pages.
    - The user can set "number of rows to display" to 25, 50, or 100
- Saving data
    - Primary key values should not be settable.
    - All other values settable to what api allows.
