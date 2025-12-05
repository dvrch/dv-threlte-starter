#!/bin/bash
# Test script for Vercel deployment verification

set -e

VERCEL_URL="https://dv-threlte-starter.vercel.app"
LOCAL_URL="http://localhost:8000"

echo "════════════════════════════════════════════════════════════════"
echo "🧪 VERCEL DEPLOYMENT TEST SCRIPT"
echo "════════════════════════════════════════════════════════════════"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=$3
    
    echo -e "\n${YELLOW}Testing${NC}: $name"
    echo "URL: $url"
    
    response=$(curl -s -w "\n%{http_code}" "$url" 2>&1)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✅ HTTP $http_code${NC}"
        if [ ! -z "$body" ]; then
            echo "Response:"
            echo "$body" | head -c 500
            echo ""
        fi
        return 0
    else
        echo -e "${RED}❌ HTTP $http_code (expected $expected_code)${NC}"
        echo "Response:"
        echo "$body" | head -c 500
        echo ""
        return 1
    fi
}

echo -e "\n${YELLOW}================================${NC}"
echo "🖥️  LOCAL TESTS"
echo -e "${YELLOW}================================${NC}"

# Test local health check
test_endpoint "Local Health Check" "$LOCAL_URL/health/" "200" || echo "⚠️  Local Django not running"

# Test local API
test_endpoint "Local API" "$LOCAL_URL/api/geometries/" "200" || echo "⚠️  Local API not responding"

echo -e "\n${YELLOW}================================${NC}"
echo "☁️  VERCEL TESTS (Production)"
echo -e "${YELLOW}================================${NC}"

# Test Vercel health check
test_endpoint "Vercel Health Check" "$VERCEL_URL/health/" "200"

# Test Vercel API
test_endpoint "Vercel API Geometries" "$VERCEL_URL/api/geometries/" "200"

# Test Vercel API Types
test_endpoint "Vercel API Types" "$VERCEL_URL/api/types/" "200"

# Test Vercel frontend
test_endpoint "Vercel Frontend" "$VERCEL_URL/app" "200"

echo -e "\n${YELLOW}================================${NC}"
echo "✨ TEST SUMMARY"
echo -e "${YELLOW}================================${NC}"

echo -e "\n${GREEN}All tests completed!${NC}"
echo ""
echo "If all endpoints returned 200, your deployment is working!"
echo ""
echo "Frontend should load geometries at: $VERCEL_URL/app"
echo ""
