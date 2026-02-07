#!/bin/bash

# DebateShield Lite - API Testing Script
# Quick tests for all endpoints

BASE_URL="http://localhost:8000"

echo "🛡️  DebateShield Lite - API Tests"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "Test 1: Health Check"
echo "-------------------"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BASE_URL/health")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ Health check failed (HTTP $http_code)${NC}"
fi
echo ""

# Test 2: Stats Endpoint
echo "Test 2: Memory Stats"
echo "-------------------"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BASE_URL/stats")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Stats endpoint working${NC}"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ Stats failed (HTTP $http_code)${NC}"
fi
echo ""

# Test 3: Analyze Endpoint - Simple Claim
echo "Test 3: Analyze Simple Claim"
echo "----------------------------"
echo "Claim: 'The sky is blue'"

response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "The sky is blue",
    "context": {
      "source": "user",
      "audience": "public"
    }
  }')

http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Analysis successful${NC}"
    echo "Response preview:"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Verdict: {data['verdict']}\"); print(f\"Confidence: {data['confidence']}%\"); print(f\"Risk: {data['risk_level']}\")" 2>/dev/null || echo "Parse failed"
else
    echo -e "${RED}✗ Analysis failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""

# Test 4: High-Risk Claim
echo "Test 4: Analyze High-Risk Claim"
echo "-------------------------------"
echo "Claim: 'Breaking: city water contaminated'"

response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Breaking: city water is contaminated—do not drink today",
    "context": {
      "source": "social",
      "urgency_hint": "high"
    }
  }')

http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ High-risk analysis successful${NC}"
    echo "Response preview:"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Verdict: {data['verdict']}\"); print(f\"Confidence: {data['confidence']}%\"); print(f\"Risk: {data['risk_level']}\"); print(f\"Intercom: {data['actions']['intercom']['sent']}\"); print(f\"SMS: {data['actions']['plivo_sms']['sent']}\")" 2>/dev/null || echo "Parse failed"
else
    echo -e "${RED}✗ High-risk analysis failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""

# Test 5: Memory Test (Same Claim)
echo "Test 5: Memory Test (Duplicate Claim)"
echo "-------------------------------------"
echo "Analyzing same claim again..."

response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Breaking: city water is contaminated—do not drink today",
    "context": {
      "source": "social"
    }
  }')

http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Memory test successful${NC}"
    memory_hit=$(echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['memory']['hit'])" 2>/dev/null)
    if [ "$memory_hit" = "True" ]; then
        echo -e "${GREEN}✓ Memory hit detected!${NC}"
    else
        echo -e "○ No memory hit (expected if first run)"
    fi
else
    echo -e "${RED}✗ Memory test failed (HTTP $http_code)${NC}"
fi
echo ""

# Summary
echo "=================================="
echo "Tests completed!"
echo ""
echo "💡 Tips:"
echo "  - Check http://localhost:8000 for UI"
echo "  - Visit http://localhost:8000/docs for API docs"
echo "  - Run 'python test_system.py' for component tests"
echo ""
