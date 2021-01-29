# sqlalchemy-challenge
Repo_for_sqlalchemy_HW

This challenge is about surfers and surfing. It was quite interesting, but a lot of researching to put solutions together. The challenge involved the using Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. The following parts give accompanying analysis:

Step 1:
1. Used the provided starter notebook and hawaii.sqlite files to complete the climate analysis and data exploration
2. Imported and used SQLAlchemy create_engine to connect the sqlite DB
3. Linked Python to the database

Precipitation Analysis:
1. Queried last 12 months of precipitation data, load the query results into a Pandas DF and plotted in a frequency graph. 
2. Precipitation frequency showed maximum precipitation around the same time every year.

Station Analysis:
1. Performed a query of stations dataset for stations and counted observation counts for unique stations.
2. Queried the DB for most active station, obtained lowest, highest and average temperature.
3. Queried the DB for last 12 months of temperature observation data, sorted by highest number of observations and plotted results in a histogram.
4. Histogram plot showed that the temperature was mostly around 75 deg Farenheit for most of the observations.

Step 2:
Used VS code to produce and design a Flask API based on queries in Step 1.
Flask was used to design routes, generate endpoints and JSONIFY the endpoints.
