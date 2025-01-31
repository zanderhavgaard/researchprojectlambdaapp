# Invoking lambdas using curl

Commands expect you to have a valid api key and the url, you should set them as environment vars:
    - `aws_api_key` for the key token
    - `aws_api_gateway` for the api url

## Putter

TODO

## Getter

Gets filenames and file urls from s3 bucket.

lives at `<api_gateway>/live/getter`, valid methods are `GET`

Must pass a json of two keys and one extra conditional key:

`StatusCode` - must be 200
`command` - must be either:
    - `list` - will return a list of all filenames in bucket.
    - `get_file_url` - will return an absolute url to the image file in the s3 bucket
      - you must also pass an extra key:value `filename` which is the name of the file.

### Example using command `list`

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "command":"list"}' "$aws_api_gateway/live/getter"
```

### Example using command `get_file_url`
```bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "command":"get_file_url","filename":"green.png"}' "$aws_api_gateway/live/getter"
```


## FeedGenerator

Generates a feed json object by quering Getter lambda.

lives at `<api_gateway>/live/feed-generator`, valid methods are `GET`

Must pass a json of two keys:
    -`StatusCode` - which should be `200`
    - `num_items` - which should either be the string `"all"` or an integer

### Example generating a feed of all available posts

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "num_items":"all"}' "$aws_api_gateway/live/feed-generator"
```


### Example of generating a feed of 10 posts

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "num_items":"10"}' "$aws_api_gateway/live/feed-generator"
```


## FeedWebView

TODO finish

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" "$aws_api_gateway/live/feed"
```

### Example generating a feed of all available posts

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "num_items":"all"}' "$aws_api_gateway/live/feed"
```


### Example of generating a feed of 10 posts

``` bash
curl -v -X GET -H "x-api-key: $aws_api_key" -H "Content-Type:application/json" -d '{"StatusCode": 200, "num_items":"10"}' "$aws_api_gateway/live/feed"
```
