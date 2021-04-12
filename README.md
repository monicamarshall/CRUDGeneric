# CRUDGeneric
Python django project that manages Conference Speaker model objects. The project uses Python 3.6, Django 2.2.10, and djangorestframework 3.9.2

This project includes a bulkload service that reads Speaker data stored in a csv file (speakers.csv, speakers2.csv in media directory) and bulkloads it to a postgres database.

Two Methods are available to bulkload the database:

Postgres native copy_from, which loads over 20,000 records in about 80 milliseconds.
Django ORM bulk_create which loads over 20,000 records in about 2 seconds.
Clearly, the Postgres native copy_from utility is lightning fast and outperforms every other bulkloading methods.

All bulkloading use flat data files, csv files. The separator ( , | ) chosen is set at the time the csv file is read.

The Speaker csv file is produced offline by dumping Speaker database rows to a csv file using the PGAdmin admin web interface, specifically the Export data option.

Every database offers the option of exporting data from a database table to a csv file.

The csv Speaker file is stored in the Media directory. In the Media directory there are 2 csv files. speakers2.csv has 20250 records.

This project allows create/update/delete/retrieve of Speaker objects.

Pagination is set at 100 records per page. ( See Settings.py for default pagination, and custom pagination StandardResultsSetPagination in crudgenerics.views

Access the Speaker service at: http://localhost:8088/speakers (The port is decided at the time the server is started)

Access to the Speaker bulkload service is available at: http://localhost:8088/bulkload
