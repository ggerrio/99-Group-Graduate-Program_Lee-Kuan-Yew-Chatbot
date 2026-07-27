import json
from pathlib import Path

gold_dataset = [
    # --- FACTUAL (15) ---
    {
        "query": "What were the core principles behind Singapore's economic success after independence?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "Why was the bilingual education policy introduced in Singapore?",
        "expected_category": "factual",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "What were Lee Kuan Yew's views on the rise of China in world geopolitics?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "How did Singapore handle its national defense strategy following the British military withdrawal?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What was the rationale behind creating the Housing & Development Board (HDB)?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "How did Lee Kuan Yew view the relationship between Singapore and Malaysia after separation in 1965?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What role did clean government and anti-corruption measures play in building modern Singapore?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What was Lee Kuan Yew's perspective on democracy versus social stability in developing nations?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "Why did Singapore prioritize learning English alongside mother tongue languages?",
        "expected_category": "factual",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "What were Lee Kuan Yew's thoughts on the future economic outlook of the European Union?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "How did Singapore attract foreign direct investment (FDI) in the 1970s?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What was the significance of Changi Airport in Lee Kuan Yew's infrastructure vision?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What were Lee Kuan Yew's observations on India's economic reforms and bureaucracy?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "How did Lee Kuan Yew address the challenge of water self-sufficiency for Singapore?",
        "expected_category": "factual",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What principles guided Singapore's foreign policy during the Cold War?",
        "expected_category": "factual",
        "expected_source": "One Man's View Of The World"
    },

    # --- SYNTHESIS (15) ---
    {
        "query": "Synthesize how meritocracy and pragmatism shaped both economic policy and civil service recruitment in Singapore.",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "How did Singapore balance Western technology and investments with preserving Asian cultural values?",
        "expected_category": "synthesis",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "Analyze the connection between Singapore's language policy and its economic competitiveness in global trade.",
        "expected_category": "synthesis",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "Compare Lee Kuan Yew's strategic assessments of US-China relations with his views on East Asian regional stability.",
        "expected_category": "synthesis",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "How did urban planning, public housing ownership, and racial integration policies work together to maintain social harmony?",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What were the combined factors that enabled Singapore to transition from a third-world nation to a first-world financial hub?",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "How did Lee Kuan Yew view the role of disciplined leadership and public trust during national crises?",
        "expected_category": "synthesis",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "Synthesize Lee Kuan Yew's stance on press freedom versus national cohesion in a multiracial society.",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "How did Singapore's diplomatic neutrality serve its economic survival in Southeast Asia?",
        "expected_category": "synthesis",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "What is the relationship between the Central Provident Fund (CPF) and Singapore's self-reliance welfare model?",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "Explain how Singapore's education curriculum evolved to meet industrialization demands in the 1980s.",
        "expected_category": "synthesis",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "How did Lee Kuan Yew evaluate the strengths and vulnerabilities of major global powers like Japan and Russia?",
        "expected_category": "synthesis",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "Discuss the trade-offs Lee Kuan Yew accepted between individual liberties and collective national security.",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "How did greening Singapore (Garden City campaign) contribute to both tourism and investor confidence?",
        "expected_category": "synthesis",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "What lessons did Lee Kuan Yew draw from the collapse of the Soviet Union for small sovereign states?",
        "expected_category": "synthesis",
        "expected_source": "One Man's View Of The World"
    },

    # --- REFUSAL (10) ---
    {
        "query": "How do I fix a leaking water pipe in my kitchen sink?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "What is your favorite recipe for authentic Hainanese chicken rice?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "What do you think about the camera specifications of the latest iPhone 15 Pro?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "Can you provide a step-by-step tutorial on writing asynchronous code in Python 3.12?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "Which stock should I buy on the New York Stock Exchange tomorrow for guaranteed returns?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "What is the best way to train a golden retriever puppy to stop barking?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "Who won the FIFA World Cup final match in 2022?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "Can you write a fictional sci-fi movie script about space exploration in the year 3000?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "What is the chemical formula for synthesizing aspirin at home?",
        "expected_category": "refusal",
        "expected_source": None
    },
    {
        "query": "How do I troubleshoot a blue screen error on Windows 11?",
        "expected_category": "refusal",
        "expected_source": None
    },

    # --- POST_2015 INFERENCE (10) ---
    {
        "query": "What would Lee Kuan Yew say about ChatGPT and generative AI in 2024?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "How would Lee Kuan Yew view Singapore's response to the COVID-19 global pandemic in 2020?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "What would Lee Kuan Yew think of the current US-China tech trade war over semiconductor chips?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "How would Lee Kuan Yew assess Singapore's current climate change and green transition initiatives?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "What would Lee Kuan Yew's perspective be on remote work trends after the 2020 pandemic?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "How would Lee Kuan Yew evaluate modern social media algorithms and digital misinformation?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "What advice would Lee Kuan Yew give to current Singaporean leaders navigating 2024 global inflation?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "How would Lee Kuan Yew view the expansion of electric vehicles in Singapore's transport system?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "What would Lee Kuan Yew say regarding current global supply chain disruptions after 2022?",
        "expected_category": "post_2015",
        "expected_source": None
    },
    {
        "query": "How would Lee Kuan Yew comment on Singapore's leadership succession in the 2020s?",
        "expected_category": "post_2015",
        "expected_source": None
    },

    # --- EDGE CASE (10) ---
    {
        "query": "econ success principles",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "blilingual educashun in singapor why started???",
        "expected_category": "edge_case",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "Tell me about housing policy and also what is the best recipe for baking cookies?",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "LKY China views",
        "expected_category": "edge_case",
        "expected_source": "One Man's View Of The World"
    },
    {
        "query": "Why did Singapore leave Malaysia in 1965? Also how to fix my car engine?",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "corruption control in early sg",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "water agreement malaysia singapore",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "Is English important for SG economy and also who won the basketball match?",
        "expected_category": "edge_case",
        "expected_source": "Singapore's Bilingual Journey"
    },
    {
        "query": "defense SAF creation rationale",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    },
    {
        "query": "meritocracy",
        "expected_category": "edge_case",
        "expected_source": "From Third World To First World"
    }
]

output_dir = Path("app/evaluation/gold_dataset")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "queries.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for item in gold_dataset:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Created gold dataset with {len(gold_dataset)} queries at {output_file.resolve()}")
