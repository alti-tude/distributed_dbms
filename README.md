# Distributed Database Systems Phase 1

**Team Name:** Samosa

**Team Members:** Kartik Gupta (20171018), Sanjana Sunil (20171027)

## Report

The report containing diagrams, fragmentation types, allocation mapping, printout of system catalog etc. can be seen in `Report.pdf`. 

## System Catalog

The system catalog has been created on all three servers. The SQL script for creation and population can be seen in `src/system_catalog.sql`. 

In addition, the functions for retrieving fragments and sites can be seen in `src/system_catalog_procedures.sql`.

### SQL API
* Fragments can be retrieved as follows, where the relation name could be Movie, User etc.:
``` SQL
> CALL getFragments('<Relation Name>')
```
* Sites can be retrieved as follows, with argument as the name of fragment
```SQL
> CALL getSites('<Fragment Name>')
```

### Python Interface
`src/DDBMS` contains the main python interface scripts.

* Fragments can be retrieved as follows, where the relation name could be Movie, User etc.:
```bash
python src/DDBMS/QuerySystemCatalog.py --get-fragments --server-config <Ralation Name>
```
* Sites can be retrieved as follows, with argument as the name of fragment
```bash
python src/DDBMS/QuerySystemCatalog.py --get-sites --server-config <Fragment ID>
```

## Application Database

Each server is thought as being in Hyderabad, Delhi or Mumbai. To create the tables, use the script `src/<City Name>/movie_db_tables.sql`. To populate with sample data, use `src/<City Name>/small_populate.sql`. This has been created in their respective servers.

