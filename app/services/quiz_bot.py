
from google import genai

def quiz_bot_response(userId: str) -> str:
    """
    Generate a response from the quiz bot using Google Generative AI (Gemini).
    """
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()
    
    # Create prompt for environment sustainability quiz
    prompt = """You are an environment sustainability quiz bot. Generate 10 multiple-choice questions to test their knowledge about environmental sustainability, recycling, or eco-friendly practices. Return the response as a JSON array. The following is an example set of 10 questions:
[
  {
    "id": 1,
    "question": "What percentage of the world's electricity comes from renewable sources?",
    "options": ["15%", "28%", "42%", "55%"],
    "correctAnswer": 1,
    "ecoFact": "Renewable energy now accounts for 28% of global electricity generation!"
  },
  {
    "id": 2,
    "question": "How much energy does recycling aluminum save compared to producing new aluminum?",
    "options": ["50%", "75%", "95%", "99%"],
    "correctAnswer": 2,
    "ecoFact": "Recycling aluminum saves 95% of the energy compared to producing new aluminum!"
  },
  {
    "id": 3,
    "question": "What is the most effective way to reduce your carbon footprint?",
    "options": ["Recycling more", "Using LED bulbs", "Eating less meat", "Taking shorter showers"],
    "correctAnswer": 2,
    "ecoFact": "Reducing meat consumption can cut your carbon footprint by up to 73%!"
  },
  {
    "id": 4,
    "question": "How long does it take for a plastic bottle to decompose?",
    "options": ["50 years", "100 years", "450 years", "1000 years"],
    "correctAnswer": 2,
    "ecoFact": "Plastic bottles take up to 450 years to decompose in landfills!"
  },
  {
    "id": 5,
    "question": "What percentage of ocean plastic pollution comes from land-based sources?",
    "options": ["40%", "60%", "80%", "95%"],
    "correctAnswer": 2,
    "ecoFact": "About 80% of ocean plastic pollution originates from land-based sources!"
  },
  {
    "id": 6,
    "question": "Which transportation method has the lowest carbon emissions per mile?",
    "options": ["Electric car", "Bus", "Train", "Bicycle"],
    "correctAnswer": 3,
    "ecoFact": "Bicycles produce zero emissions and are the most eco-friendly transport option!"
  },
  {
    "id": 7,
    "question": "How much water can a single dripping faucet waste per year?",
    "options": ["100 gallons", "500 gallons", "1,000 gallons", "3,000 gallons"],
    "correctAnswer": 2,
    "ecoFact": "A single dripping faucet can waste over 3,000 gallons of water per year!"
  },
  {
    "id": 8,
    "question": "What percentage of food produced globally is wasted?",
    "options": ["10%", "20%", "33%", "50%"],
    "correctAnswer": 2,
    "ecoFact": "About one-third of all food produced globally is wasted, contributing to climate change!"
  },
  {
    "id": 9,
    "question": "Which renewable energy source is growing the fastest worldwide?",
    "options": ["Wind", "Solar", "Hydroelectric", "Geothermal"],
    "correctAnswer": 1,
    "ecoFact": "Solar energy is the fastest-growing renewable energy source globally!"
  },
  {
    "id": 10,
    "question": "How many trees does it take to offset the CO2 from one car per year?",
    "options": ["5 trees", "15 trees", "31 trees", "50 trees"],
    "correctAnswer": 2,
    "ecoFact": "It takes about 31 trees to offset the CO2 emissions from one car per year!"
  }
]
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=prompt
    )
    
    return response.text



