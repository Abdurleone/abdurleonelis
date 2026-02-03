# Multi-stage build for React frontend
FROM node:18.17.1-alpine3.18 as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build optimized production bundle
RUN npm run build

# Production stage - serve with Nginx
FROM nginx:alpine

# Copy built application to Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
