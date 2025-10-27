🏦 PDF Policy Underwriting Agent

This project is a command-line tool that reads a loan policy PDF, extracts its lending criteria using Google Gemini, and automatically decides whether a loan application should be approved or denied. It parses rules like credit score thresholds, income minimums, and debt-to-income limits, then applies them to real applicant data with clear reasoning and explanations.

🧰 Tools Used

I built this project mainly in Python, using the following tools and libraries:

- Google Gemini 2.5 Flash – for reading and structuring the policy PDF.
- pdfminer.six – to extract text from PDFs.
- pydantic – for data validation and schema management.
- tenacity – for retry logic in case of API or parsing errors.
- dotenv – to manage API keys and environment variables.
- argparse & json – for command-line arguments and clean output formatting.

🧠 Thought Process / Architecture

The goal was to create a simple underwriting system that could:

1. Read a lending policy from a PDF file
2. Understand its lending rules (credit tiers, income minimums, DTI thresholds)
3. Apply those rules to evaluate a loan application automatically.

The code is structured into small, focused modules:

- policy_extractor.py gets raw text from the PDF.
- llm_parser.py uses Gemini to turn that text into structured rules.
- decision_engine.py runs the actual approval logic based on the applicant’s data.
- cli.py ties it all together so it can be run easily from the terminal.

It’s designed to be modular, so each piece can be swapped out later—for example, replacing Gemini with OpenAI or adding a web interface.

🚀 Future Improvements & Challenges

There’s a lot of room to grow:

- Better LLM parsing – fine-tune prompts to handle complex or messy PDF wording.
- Multiple applicants – batch processing for a folder of loan applications.
- Explainability – generate more human-like explanations of approval/denial reasons.
- Interface – turn this into a small dashboard or API service.
- Error handling – smarter fallback logic if the model output is incomplete.

⚙️ How to Run the Code

1. Clone the repository

git clone https://github.com/<your-username>/athena-underwriting-agent.git
cd athena-underwriting-agent

2. Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate   # On Mac/Linux
# or
.venv\Scripts\activate      # On Windows

3. Install the dependencies

pip install -r requirements.txt

4. Set up your environment variables
Copy .env.example → .env and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash

5. Run the underwriting agent

python -m src.cli --policy data/loan_policy.pdf --app examples/sample_app.json

6. View the results

The tool will print a formatted underwriting decision, including:
- Approval or denial result
- Reasoning breakdown (credit, DTI, employment)
- Applied policy rules
- JSON output and trace log for transparency