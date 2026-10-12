# ProposalDetail


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
**votes** | [**List[VoteOut]**](VoteOut.md) |  | [optional] 

## Example

```python
from voting_sdk.models.proposal_detail import ProposalDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ProposalDetail from a JSON string
proposal_detail_instance = ProposalDetail.from_json(json)
# print the JSON string representation of the object
print(ProposalDetail.to_json())

# convert the object into a dict
proposal_detail_dict = proposal_detail_instance.to_dict()
# create an instance of ProposalDetail from a dict
proposal_detail_from_dict = ProposalDetail.from_dict(proposal_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


