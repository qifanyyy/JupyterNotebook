from math import log

rates = (
    # PLN, EUR, USD, RUB
    (1, 0.23, 0.26, 17.41),  # PLN
    (4.31, 1, 1.14, 75.01),  # EUR
    (3.79, 0.88, 1, 65.93),  # USD
    (0.057, 0.013, 0.015, 1),  # RUB
)

currencies = ('PLN', 'EUR', 'USD', 'RUB')


def arbitrage(graph):

    # Converting each edge to log(edge)
    transformed_graph = [[-log(edge) for edge in row] for row in graph]

    # Pick any source vertex -- we can run Bellman-Ford from any vertex and
    # get the right result
    source = 0

    # Get length of the graphs list
    n = len(transformed_graph)
    print(f'Length {n}')

    # Set minimum distance to infinity for all the graphs
    min_dist = [float('inf')] * n
    print(f'Minimum distance {min_dist}')

    # Minimum distance for the source set to 0
    min_dist[source] = 0
    print(f'Minimum distance for the source set to 0 - {min_dist}')

    # Relax edges |V - 1| times
    for loop in range(n - 1):
        print(f'Loop {loop}')

        for source_currency in range(n):
            # print(f'Loop for source currency {currencies[source_currency]}')

            for dest_currency in range(n):
                # print(f'Loop for {currencies[source_currency]} -> {currencies[dest_currency]}')

                if min_dist[dest_currency] > min_dist[source_currency] + transformed_graph[source_currency][dest_currency]:
                    print(f"Cheaper route found: {currencies[source_currency]} -> {currencies[dest_currency]}")
                    print(f'Latest cost was {min_dist[dest_currency]}')
                    min_dist[dest_currency] = min_dist[source_currency] + transformed_graph[source_currency][dest_currency]
                    print(f'New cost {min_dist[source_currency]}+{transformed_graph[source_currency][dest_currency]}={min_dist[dest_currency]}')
                    print('=== === ===')

    for row in transformed_graph:
        print(row)
    print('-----------')
    print(min_dist)

    # If we can still relax edges, then we have a negative cycle
    for source_currency in range(n):
        for dest_currency in range(n):
            if min_dist[dest_currency] > min_dist[source_currency] + transformed_graph[source_currency][dest_currency]:
                print(f'Found arbitrage: {currencies[source_currency]} -> {currencies[dest_currency]}')


if __name__ == "__main__":
    arbitrage(rates)
