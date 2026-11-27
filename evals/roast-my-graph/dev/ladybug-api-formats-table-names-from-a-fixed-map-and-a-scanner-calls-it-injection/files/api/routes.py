"""Flask routes for the breeders' pages. Login is handled by the reverse proxy in front of the API."""
from flask import Flask, abort, jsonify, request

import ladybug

from . import browse

app = Flask(__name__)
db = ladybug.Database("/srv/fieldbook/fieldbook.lbdb", read_only=True)


def connection():
    return ladybug.Connection(db)


@app.get("/api/<kind>")
def list_route(kind):
    try:
        rows = browse.list_nodes(connection(), kind,
                                 skip=request.args.get("skip", 0, type=int),
                                 limit=request.args.get("limit", 50, type=int))
    except browse.NotFound:
        abort(404)
    return jsonify(rows)


@app.get("/api/<kind>/<key_value>")
def get_route(kind, key_value):
    try:
        return jsonify(browse.get_node(connection(), kind, key_value))
    except browse.NotFound:
        abort(404)


@app.get("/api/<kind>/<key_value>/<link>")
def follow_route(kind, key_value, link):
    if link not in browse.LINKS or browse.LINKS[link][0] != browse.TABLES.get(kind, (None,))[0]:
        abort(404)
    return jsonify(browse.follow(connection(), link, key_value,
                                 limit=request.args.get("limit", 50, type=int)))
