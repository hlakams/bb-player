"""
Assorted utilities for benchmarking agent/strategy performance
"""

# update win likelihood
def win_likelihood_update(prior: float, current: float, batch_no: int) -> float:
    if batch_no == 1:
        return current
    else:
        return (((batch_no - 1) * prior + current) / batch_no)

def update_results(previous_result: list, current_result: list, batch_no: int) -> list:
    return [
            # name
            current_result[0],
            # games
            previous_result[1] + current_result[1],
            # wins
            previous_result[2] + current_result[2],
            # losses
            previous_result[3] + current_result[3],
            # draws
            previous_result[4] + current_result[4],
            # win likelihood update
            win_likelihood_update(previous_result[5], current_result[5], batch_no),
            # new balance
            current_result[6]
        ]