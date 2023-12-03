wrk.method = "POST"
wrk.body   = '{"first_name": "^J.*", "last_name": ".*o.*"}'
wrk.headers["Content-Type"] = "application/json"
