# VoteCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voter_name** | **str** |  | 
**vote** | [**VoteChoice**](VoteChoice.md) |  | 

## Example

```python
from voting_sdk.models.vote_create import VoteCreate

# TODO update the JSON string below
json = "{}"
# create an instance of VoteCreate from a JSON string
vote_create_instance = VoteCreate.from_json(json)
# print the JSON string representation of the object
print(VoteCreate.to_json())

# convert the object into a dict
vote_create_dict = vote_create_instance.to_dict()
# create an instance of VoteCreate from a dict
vote_create_from_dict = VoteCreate.from_dict(vote_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


