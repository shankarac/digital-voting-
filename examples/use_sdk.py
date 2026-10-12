"""Talk to the local voting API with the generated SDK.

Run the API first, then:
    pip install -e voting_sdk
    python examples/use_sdk.py
"""

from voting_sdk import ApiClient
from voting_sdk.api.proposals_api import ProposalsApi


def main() -> None:
    client = ApiClient()
    api = ProposalsApi(client)
    proposals = api.list_proposals()
    print(f"{len(proposals)} proposals")
    for proposal in proposals:
        print(f"- [{proposal.status}] {proposal.title}: {proposal.total_votes} votes")


if __name__ == "__main__":
    main()
