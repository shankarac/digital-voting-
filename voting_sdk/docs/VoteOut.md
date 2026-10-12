# VoteOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**proposal_id** | **int** |  | 
**voter_name** | **str** |  | 
**vote** | [**VoteChoice**](VoteChoice.md) |  | 
**voted_at** | **str** |  | 

## Example

```python
from voting_sdk.models.vote_out import VoteOut

# TODO update the JSON string below
json = "{}"
# create an instance of VoteOut from a JSON string
vote_out_instance = VoteOut.from_json(json)
# print the JSON string representation of the object
print(VoteOut.to_json())

# convert the object into a dict
vote_out_dict = vote_out_instance.to_dict()
# create an instance of VoteOut from a dict
vote_out_from_dict = VoteOut.from_dict(vote_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


