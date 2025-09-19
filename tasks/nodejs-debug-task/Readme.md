# nodejs-debug-task

## Summary
Small Node.js terminal-first debugging task. The baseline Node server crashes on `/greet` due to Express-style access to `req.query`. Fix the server so it starts and passes the included tests.

## Quickstart
1. `cd tasks/nodejs-debug-task`
2. (Optional) `docker build -t nodejs-debug-task .`
3. `./run-tests.sh` — runs pytest and exits 0 on success.

## Domain
Bug-fix / troubleshooting for small Node.js service.

## Caveats
- The oracle/solution is available in `solution.sh`. **Do not** copy/run it from inside runtime images used by the tests.
- No network is required at runtime: only Node built-ins and pytest/requests (Python) are used.