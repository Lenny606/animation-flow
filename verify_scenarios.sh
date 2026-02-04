
# Script to verify the Scenario Generation endpoints
# Usage: ./verify_scenarios.sh

echo "Verifying Scenario Generation Agent..."

# Test 1: Generate a Scenario (Mocking might be needed if no API key)
# For now, we will just check if the endpoint is reachable and validation works.
# If you have an API key, it might actually charge you, so be careful. 
# We'll rely on the fact that if it returns 401/403 (Invalid Key) or 500 (with proper provider error), 
# then the code path is working.

echo "Test 1: Check endpoint existence and validation"
curl -X POST "http://localhost:8000/scenarios/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "topic": "Future of Mars Colonization", 
           "style": "Documentary",
           "target_audience": "Students",
           "duration": 30,
           "llm_provider": "openai"
         }'
echo -e "\n"

echo "Test 2: Check with missing fields (should fail validation)"
curl -X POST "http://localhost:8000/scenarios/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "topic": "Just a topic"
         }'
echo -e "\n"

echo "Verification script finished."
