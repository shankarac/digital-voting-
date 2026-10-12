# ProposalCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | 
**deadline** | **datetime** | UTC deadline. Defaults to 2 days from now when omitted. | [optional] 

## Example

```python
from voting_sdk.models.proposal_create import ProposalCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ProposalCreate from a JSON string
proposal_create_instance = ProposalCreate.from_json(json)
# print the JSON string representation of the object
print(ProposalCreate.to_json())

# convert the object into a dict
proposal_create_dict = proposal_create_instance.to_dict()
# create an instance of ProposalCreate from a dict
proposal_create_from_dict = ProposalCreate.from_dict(proposal_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


