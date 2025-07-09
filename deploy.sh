#!/bin/bash

# Deployment script for Render
echo "Starting deployment process..."

# Build frontend
echo "Building frontend..."
cd frontend
npm install --force
npm run build
cd ..

# Copy frontend build to Flask static folder
echo "Copying frontend build to Flask static folder..."
rm -rf src/static/*
cp -r frontend/dist/* src/static/

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Deployment preparation complete!"
echo "Your project is ready to be deployed on Render."

