import random

def simulate_bandwidth(num_routers, 
                       bandwidth_per_router_gbps, 
                       num_users, 
                       normal_bandwidth_range, 
                       peak_bandwidth, 
                       spike_percentage_range, 
                       simulations=1000,
                       verbose=False):
    total_bandwidth_mbps = num_routers * bandwidth_per_router_gbps * 1000
    failures = 0

    for run in range(simulations):
        spike_percentage = random.randint(*spike_percentage_range)
        num_spike_users = num_users * spike_percentage // 100
        spike_users = set(random.sample(range(num_users), num_spike_users))

        user_bandwidths = [
            peak_bandwidth if i in spike_users else random.randint(*normal_bandwidth_range)
            for i in range(num_users)
        ]

        total_required_bandwidth = sum(user_bandwidths)

        if verbose:
            print(f"Run {run+1}: Required {total_required_bandwidth} Mbps, Available {total_bandwidth_mbps} Mbps")

        if total_required_bandwidth > total_bandwidth_mbps:
            failures += 1

    failure_percent = (failures / simulations) * 100
    print(f"Simulations run: {simulations}")
    print(f"Bandwidth insufficient in {failures} runs ({failure_percent:.2f}% of the time)")
    print(f"Bandwidth sufficient in {simulations - failures} runs ({100 - failure_percent:.2f}% of the time)")

    return {
        "simulations": simulations,
        "failures": failures,
        "failure_percent": failure_percent
    }

simulate_bandwidth(
    num_routers=2,
    bandwidth_per_router_gbps=1,
    num_users=35,
    normal_bandwidth_range=(40, 50),
    peak_bandwidth=90,
    spike_percentage_range=(10, 20),
    simulations=1000
)
