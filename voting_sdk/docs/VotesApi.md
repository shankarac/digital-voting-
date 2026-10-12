# voting_sdk.VotesApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**revoke_vote**](VotesApi.md#revoke_vote) | **DELETE** /votes/{vote_id} | Revoke a vote


# **revoke_vote**
> revoke_vote(vote_id)

Revoke a vote

Deletes a vote only while its proposal is still active.

### Example


```python
import voting_sdk
from voting_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = voting_sdk.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with voting_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = voting_sdk.VotesApi(api_client)
    vote_id = 56 # int | 

    try:
        # Revoke a vote
        api_instance.revoke_vote(vote_id)
    except Exception as e:
        print("Exception when calling VotesApi->revoke_vote: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vote_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**404** | Vote not found |  -  |
**409** | Proposal is closed or expired |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

