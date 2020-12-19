# RESTful switch

Available endpoints
---
Api prefix: `/v1`

`/polls`:
 * `GET`: returns all polls ever created
 * `POST`: creates a new poll

`/poll/<string:poll_id>` (*poll_id* - ObjectId-style id of a poll):
 * `GET`: returns the details of a poll
 * `DELETE`: deletes the poll
 
`/poll/<string:poll_id>/vote` (*poll_id* - ObjectId-style id of a poll):
 * `GET`: returns the amount of votes for every option in a poll
 * `POST`: adds a vote

`/file`:
 * `POST`: uploads a file

`/file/<string:file_id>` (*file_id* - sha256 hash of a file):
 * `GET`: serves the file

Testing
---
Uploading a file from a command line:
```
curl --header "Content-Type: FILE_TYPE" --data-binary @"FILE_PATH" localhost:5000/v1/file
```  
`FILE_TYPE` - the [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) of a file
being uploaded, eg. `image/jpeg`  
`FILE_PATH` - path to the file on your pc
