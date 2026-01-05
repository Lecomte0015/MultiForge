FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy source code
COPY . .

# Run the build process to generate production CSS/JS
# Note: We run "next build" here to force Tailwind CSS compilation
RUN npm run build

# Start the application in development mode
# Next.js will use the build artifacts (including the compiled CSS)
CMD ["npm", "run", "dev"]