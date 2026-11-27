from shopfront import sqlfile


def product_page(conn, product_id):
    header = sqlfile.rows(conn, "product_page", product_id=product_id)
    # TODO: "pairs with" strip under the gallery
    return {"product": header[0] if header else None}
