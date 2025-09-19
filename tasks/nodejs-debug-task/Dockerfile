FROM node:18-alpine

WORKDIR /workspace

# copy everything (grader may build but tests are driven by run-tests.sh)
COPY . .

# install python for tests (alpine)
RUN apk add --no-cache python3 py3-pip bash

# ensure pip deps can be installed by run-tests.sh
RUN python3 -m pip install -U pip

# default entrypoint kept simple; tests are run via run-tests.sh
CMD ["/bin/sh", "-c", "ls -la && /bin/sh"]