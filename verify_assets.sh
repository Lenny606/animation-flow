
# Script to verify the Image Generation Agent endpoints
# Usage: ./verify_assets.sh

echo "Verifying Image Generation Agent..."
echo "WARNING: This will trigger DALL-E 3 unless mocked. Ensure you want to spend credits if setting is live."

# Test 1: Generate Assets from a Mock Scenario
# We pass a scenario object directly as per the API contract API
curl -X POST "http://localhost:8000/assets/generate_from_scenario" \
     -H "Content-Type: application/json" \
     -d '{
       "llm_provider": "openai",
       "scenario": {
         "_id": "test_scen_001",
         "title": "Test Scenario",
         "style": "Cyberpunk Anime",
         "scenes": [
           {
             "id": 1,
             "visual_description": "A neon-lit street in Tokyo, raining.",
             "voiceover": "The city never sleeps."
           },
           {
             "id": 2,
             "visual_description": "A cyborg detective looking at a hologram.",
             "voiceover": "But I am always watching."
           }
         ]
       }
     }'

echo -e "\nVerification script finished."
