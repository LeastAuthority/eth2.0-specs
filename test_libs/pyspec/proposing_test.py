from os import urandom
from eth2spec.phase0 import spec as e2

# note to self:
# - try in pypy, this is SLOW
# - much faster in proper Gwei scaling...
# - numbers look better too


def create_validators(balances):
    return [
        e2.Validator(
            effective_balance=balance,
        )
        for balance in balances
    ]

eth_to_gwei = 1000000000
N = 100

validator_balances_eth = [32, 1, 16, 16, 16, 16, 16, 16]
validator_balances_gwei = [e * eth_to_gwei for e in validator_balances_eth]

state = e2.BeaconState(
    validators=create_validators(validator_balances_gwei),
)

counts = [0 for _ in validator_balances_gwei]

for _ in range(N):
    proposed = e2.compute_proposer_index(
        state=state,
        indices=range(8),
        seed=bytes(urandom(8)),
    )
    counts[proposed] += 1

total_gwei = sum(validator_balances_gwei)
expected_ratios = [float(balance) / float(total_gwei) for balance in validator_balances_gwei]
ratios = [float(count) / float(N) for count in counts]
diffs = [expected - actual for expected, actual in zip(expected_ratios, ratios)]
print(expected_ratios)
print(ratios)
print(diffs)
