#!/usr/bin/env python3
"""Serves docs/ on http://localhost:4173 for looking at the site before it is published.  python3 tools/serve.py"""
import functools, http.server, os
DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DOCS)
http.server.ThreadingHTTPServer(("127.0.0.1", 4173), handler).serve_forever()
