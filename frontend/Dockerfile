# Use Node 18 as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application
COPY frontend/ .

# Build the Docusaurus site
RUN npm run build

# Expose port
EXPOSE 3000

# Serve the built site
CMD ["npm", "run", "serve"]