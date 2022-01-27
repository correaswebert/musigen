# ensure the exact baseimage is used (exemplified below)
FROM python:3.9.10-slim-bullseye

# install dumb-init for invoking docker
RUN apk add dumb-init

# optimize for production
ENV NODE_ENV production

WORKDIR /app

# 'node' process owns the files now, not 'root'
COPY --chown=node:node . .

# do not install dev dependencies
RUN npm install --only=production

# transpile .ts to .js
RUN npm run build

# make 'node' as the process owner, not 'root'
USER node

# prevent starting process as PID1 by using dumb-init
CMD ["dumb-init", "python", "run", "start"]
