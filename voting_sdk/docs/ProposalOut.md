# ProposalOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**description** | **str** |  | 
**created_at** | **str** |  | 
**deadline** | **str** |  | 
**status** | [**ProposalStatus**](ProposalStatus.md) |  | 
**yes_count** | **int** |  | [optional] [default to 0]
**no_count** | **int** |  | [optional] [default to 0]
**abstain_count** | **int** |  | [optional] [default to 0]
**total_votes** | **int** |  | [optional] [default to 0]

## Example

```python
from voting_sdk.models.proposal_out import ProposalOut

# TODO update the JSON string below
json = "{}"
# create an instance of ProposalOut from a JSON string
proposal_out_instance = ProposalOut.from_json(json)
# print the JSON string representation of the object
print(ProposalOut.to_json())

# convert the object into a dict
proposal_out_dict = proposal_out_instance.to_dict()
# create an instance of ProposalOut from a dict
proposal_out_from_dict = ProposalOut.from_dict(proposal_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


