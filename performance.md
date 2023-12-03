# Performance Comparison

## Test Environment

```lua
wrk.method = "POST"
wrk.body   = '{"first_name": "John", "last_name": "Doe"}'
wrk.headers["Content-Type"] = "application/json"
```
wrk command:
```bash
wrk -t12 -c400 -d30s -s tests/post_search_users.lua http://localhost:8000/users/users/search/
```


- Service URL: http://localhost:8000/users/users/search/
- Test Duration: 30 seconds
- Number of Threads: 12
- Number of Open Connections: 400

## Without Caching


## With Caching
Running 30s test @ http://localhost:8000/users/users/search/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   414.31ms   35.12ms 593.30ms   79.65%
    Req/Sec    93.24     76.20   323.00     64.39%
  28577 requests in 30.08s, 5.94MB read
Requests/sec:    949.92
Transfer/sec:    202.23KB



