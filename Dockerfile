# Step 1: Build the React frontend
FROM node:14 as build-frontend
WORKDIR /app/frontend
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend ./
RUN npm run build

# Step 2: Set up the backend environment
FROM python:3.9-slim as backend-base
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .env
COPY . ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# Step 3: Serve the React application
FROM node:14 as serve-frontend
RUN npm install -g serve
WORKDIR /app
COPY --from=build-frontend /app/frontend/build ./build
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
