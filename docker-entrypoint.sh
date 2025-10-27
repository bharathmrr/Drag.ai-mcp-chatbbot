#!/bin/bash
set -e

echo "=================================="
echo "🚀 AI-MCP Orchestrator Starting"
echo "=================================="

# Start backend server
cd /app/backend
echo "Starting backend server..."
python real_ai_server.py &

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 5

# Serve frontend (using Python's built-in server)
cd /app/frontend/dist
echo "Starting frontend server..."
python -m http.server 3000 &

echo "=================================="
echo "✅ All services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "=================================="

# Keep container running
wait -n

# Exit with status of process that exited first
exit $?
