
# Script to verify the Video Generation Agent endpoints
# Usage: ./verify_video.sh

echo "Verifying Video Generation Agent..."

# Test 1: Generate Video from Mock Assets
curl -X POST "http://localhost:8000/video/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "scenario_id": "test_scen_video_001",
       "provider": "mock",
       "generate_voiceover": false,
       "image_assets": [
         {
           "_id": "img_001",
           "image_url": "https://via.placeholder.com/150",
           "prompt_used": "A running robot",
           "order": 1
         }
       ]
     }'

echo -e "\nWaiting for mock generation..."

echo "Verification script finished."
