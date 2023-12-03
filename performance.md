# Performance Comparison

## Test Environment

```lua
wrk.method = "POST"
wrk.body   = '{"first_name": "^J.*", "last_name": ".*o.*"}'
wrk.headers["Content-Type"] = "application/json"
```

## params
- Service URL: http://localhost:8000/users/users/search/
- Test Duration: 30 seconds
- Number of Threads: 16
- Number of Open Connections: 60

## Without Caching
```bash
wrk -d 30 -t 16 -c 60 --latency -s utils/post_search_users.lua http://localhost:8000/users/users/search/?no_cache=true
```

```
Running 30s test @ http://localhost:8000/users/users/search/?no_cache=true
  16 threads and 60 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   114.97ms   21.88ms 272.99ms   75.36%
    Req/Sec    26.12      6.76    50.00     89.11%
  Latency Distribution
     50%  115.00ms
     75%  121.97ms
     90%  141.01ms
     99%  185.13ms
  12508 requests in 30.02s, 4.91MB read
Requests/sec:    416.61
Transfer/sec:    167.62KB
```

## With Caching
```bash
wrk -d 30 -t 16 -c 60 --latency -s utils/post_search_users.lua http://localhost:8000/users/users/search/?no_cache=false
```

```
Running 30s test @ http://localhost:8000/users/users/search/?no_cache=false
  16 threads and 60 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    51.17ms    6.59ms  97.54ms   71.48%
    Req/Sec    58.62      7.30    90.00     66.25%
  Latency Distribution
     50%   50.65ms
     75%   54.90ms
     90%   59.35ms
     99%   71.27ms
  28141 requests in 30.03s, 11.06MB read
Requests/sec:    937.21
Transfer/sec:    377.08KB
```



