# lab

Throwaway analyses for the buying team: which products bridge two otherwise separate baskets, what a range cut
would disconnect, and so on. Works on a local snapshot of the order data in an embedded graph file
(`var/baskets.kz`, built with `make snapshot`), so nothing here touches the shop's systems.

    pip install -r requirements.txt
    make snapshot
    make query Q=queries/basket_bridges.cypher
