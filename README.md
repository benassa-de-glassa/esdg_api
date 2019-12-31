This is the readme file for the API

## Routing
All API calls go through IP:5000/api/*
Currently implemented routes are:

- api/groups:
  - requires: 
    - None
  - returns a JSON object containing the DB Names

- api/dataset:
  - requires: 
    - 'groups': label of selected group 
  - returns a JSON object containing the DB files 

- api/meta:
  - requires: 
    - 'groups': label of selected group
    - 'dataset': label of selected dataset
  - returns an array of JSON objects containing the names (variables) as well as their ID codes (country_codes, etc.) for each dimension. 

- api/data:
  - requires: 
    - 'groups': label of selected group
    - 'dataset': label of selected dataset
    - '[...meta]': (multiple) selected labels of the dimensions 
  - returns an array of JSON objects containing the data of the requested  variables (dimension). 

## Future Roadmap

-api/metadata:
Will be introduced in future versions. Will offer metadata information for each datapoint