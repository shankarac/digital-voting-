# voting_sdk.ProposalsApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cast_vote**](ProposalsApi.md#cast_vote) | **POST** /proposals/{proposal_id}/vote | Cast a vote
[**close_proposal**](ProposalsApi.md#close_proposal) | **PATCH** /proposals/{proposal_id}/close | Close a proposal
[**create_proposal**](ProposalsApi.md#create_proposal) | **POST** /proposals/ | Create a proposal
[**get_proposal**](ProposalsApi.md#get_proposal) | **GET** /proposals/{proposal_id} | Get a proposal
[**list_proposals**](ProposalsApi.md#list_proposals) | **GET** /proposals/ | List proposals


# **cast_vote**
> VoteOut cast_vote(proposal_id, vote_create)

Cast a vote

One vote per voter name. A second vote is rejected with 409 until the first vote is revoked. Voting is rejected once the proposal is closed or expired.

### Example


```python
import voting_sdk
from voting_sdk.models.vote_create import VoteCreate
from voting_sdk.models.vote_out import VoteOut
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
    api_instance = voting_sdk.ProposalsApi(api_client)
    proposal_id = 56 # int | 
    vote_create = voting_sdk.VoteCreate() # VoteCreate | 

    try:
        # Cast a vote
        api_response = api_instance.cast_vote(proposal_id, vote_create)
        print("The response of ProposalsApi->cast_vote:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->cast_vote: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 
 **vote_create** | [**VoteCreate**](VoteCreate.md)|  | 

### Return type

[**VoteOut**](VoteOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**404** | Proposal not found |  -  |
**409** | Duplicate vote, or the proposal is not active |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **close_proposal**
> ProposalOut close_proposal(proposal_id, x_admin_key=x_admin_key)

Close a proposal

Admin force-close. Requires the X-Admin-Key header. Closed proposals cannot be voted on or revoked.

### Example


```python
import voting_sdk
from voting_sdk.models.proposal_out import ProposalOut
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
    api_instance = voting_sdk.ProposalsApi(api_client)
    proposal_id = 56 # int | 
    x_admin_key = 'x_admin_key_example' # str | Shared admin key. The local demo default is community-admin. (optional)

    try:
        # Close a proposal
        api_response = api_instance.close_proposal(proposal_id, x_admin_key=x_admin_key)
        print("The response of ProposalsApi->close_proposal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->close_proposal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 
 **x_admin_key** | **str**| Shared admin key. The local demo default is community-admin. | [optional] 

### Return type

[**ProposalOut**](ProposalOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**403** | Missing or invalid admin key |  -  |
**404** | Proposal not found |  -  |
**409** | Proposal is not active |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_proposal**
> ProposalOut create_proposal(proposal_create)

Create a proposal

Creates an active proposal. If deadline is omitted it is set to 2 days from now.

### Example


```python
import voting_sdk
from voting_sdk.models.proposal_create import ProposalCreate
from voting_sdk.models.proposal_out import ProposalOut
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
    api_instance = voting_sdk.ProposalsApi(api_client)
    proposal_create = voting_sdk.ProposalCreate() # ProposalCreate | 

    try:
        # Create a proposal
        api_response = api_instance.create_proposal(proposal_create)
        print("The response of ProposalsApi->create_proposal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->create_proposal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_create** | [**ProposalCreate**](ProposalCreate.md)|  | 

### Return type

[**ProposalOut**](ProposalOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proposal**
> ProposalDetail get_proposal(proposal_id)

Get a proposal

Returns one proposal, its vote counts, and the individual votes.

### Example


```python
import voting_sdk
from voting_sdk.models.proposal_detail import ProposalDetail
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
    api_instance = voting_sdk.ProposalsApi(api_client)
    proposal_id = 56 # int | 

    try:
        # Get a proposal
        api_response = api_instance.get_proposal(proposal_id)
        print("The response of ProposalsApi->get_proposal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->get_proposal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 

### Return type

[**ProposalDetail**](ProposalDetail.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Proposal not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_proposals**
> List[ProposalOut] list_proposals()

List proposals

Returns every proposal, including closed and expired ones, with current vote counts.

### Example


```python
import voting_sdk
from voting_sdk.models.proposal_out import ProposalOut
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
    api_instance = voting_sdk.ProposalsApi(api_client)

    try:
        # List proposals
        api_response = api_instance.list_proposals()
        print("The response of ProposalsApi->list_proposals:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->list_proposals: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ProposalOut]**](ProposalOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

