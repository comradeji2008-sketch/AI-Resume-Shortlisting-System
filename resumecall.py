import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from pypdf import PdfReader
from docx import Document

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client=Groq(api_key=my_api_key)


model = "openai/gpt-oss-120b"
role="user"


job_description = """
Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.

We will take your location preferences into consideration. Preferences are based on business availability and are not guaranteed. Applicants will be considered at all locations in the United States including but not limited to:

• AZ (Phoenix, Tempe)
• CA (Berkeley, Culver City, Cupertino, East Palo Alto, Irvine, Los Angeles, Manhattan Beach, Palo Alto, San Diego, San Francisco, San Jose, San Luis Obispo, Santa Barbara, Santa Clara, Santa Cruz, Santa Monica, Sunnyvale)
• CO (Boulder, Denver)
• GA (Atlanta, Kennesaw)
• IL (Chicago)
• MA (Boston, Cambridge, Hudson, North Reading, Westborough)
• MD (Baltimore)
• MI (Detroit)
• MN (Minneapolis)
• NJ (Jersey City)
• NY (New York)
• OR (Portland)
• PA (Philadelphia, Pittsburgh)
• TN (Nashville)
• TX (Austin, Dallas)
• VA (Arlington, Herndon)
• WI (Madison)
• WA (Bellevue, Seattle, Redmond)
During your application, you will have the opportunity to highlight your expertise in one or more of these specialized areas:

• Machine Learning • Distributed Systems and Data Management • Database Systems • Quantum Computing • Network Development • Query Processing and Optimization • Automated Reasoning • Embedded Systems • Data Engineering • Mobile Development • Game Development

While team placement is based on business needs, sharing your specific skills and interests helps us better align your experience with potential roles.

Applications are reviewed on a rolling basis. For an update on your status or to confirm your application was submitted successfully, please login to your candidate portal at Amazon.jobs. Amazon works with a high volume of applicants so we appreciate your patience as we review applications.


Key job responsibilities
• Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
• Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
• Participate in code reviews and contribute to technical documentation.
• Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
• Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
• Write clean, maintainable code following best practices and design patterns.
• Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
• Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.

Basic Qualifications
- Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
- Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
- Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
- Must be 18 years of age of older

Preferred Qualifications
- Experience from previous technical internship(s) or demonstrated project experience
- Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
- Demonstrated ability to learn and adapt to new technologies quickly
- Basic understanding of software development lifecycle (SDLC)
- Strong problem-solving and analytical skills
- Excellent written and verbal communication skills

Amazon is an equal opportunity employer and does not discriminate on the basis of protected veteran status, disability, or other legally protected status.

Our inclusive culture empowers Amazonians to deliver the best results for our customers. If you have a disability and need a workplace accommodation or adjustment during the application and hiring process, including support for the interview or onboarding process, please visit https://amazon.jobs/content/en/how-we-hire/accommodations for more information. If the country/region you’re applying in isn’t listed, please contact your Recruiting Partner.

"""

class jobD(BaseModel):
    role: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience: float | None = None
    educational_requirements: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


jobD_schema = jobD.model_json_schema()

# assigning system to evaluate the job

system_prompt = f"""
You're an expert HR assistant .
Your job is to analyze job descriiption and extract structured information from them.

Return ONLY valid JSON matching this schema
{jobD_schema}
IMPORTANT :
DO NOT return the schema itself.
DO NOT return fields like "properties ", "tittle" or "types"
fill the schema with actual information from the job description.

If minimum experience is not required then return none
If information for a list is missing return an empty list .

Do not invent information.

"""

user_prompt = f"""
Analyze the following job description.
{job_description}

"""
messages_system = {
    "role": "system",
    "content" : system_prompt
}

messages_user = {
    "role": "user",
    "content": user_prompt
}

response_format = {
    "type" :"json_object"
}

messages = [messages_system, messages_user]
response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format=response_format
    )

final_answer = response.choices[0].message.content
#print(final_answer)

raw_json = final_answer

job_data = json.loads(raw_json)

job = jobD(**job_data)

print(job.minimum_experience)
print(job.educational_requirements)

#parse real part 2 pe aagye resume matching

class Match_result(BaseModel):
    score: float
    details: dict
class Experience(BaseModel):
    company :str|None= None
    role : str|None  = None
    duration:str |None = None
    description :str|None = None
    skills_used :str|None = None

class Resume (BaseModel):
    name : str|None = None
    email:str|None = None
    phone: str | None = None

    total_experience: str|None =None

    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


resume_schema = Resume.model_json_schema()
def final_score (job, resume):

    match_schema = Match_result.model_json_schema()

    prompt = f"""

    You are an HR recruiter.

    Compare the candidate's resume with the job description.
    Job_description:
    {job.model_dump_json(indent = 2)}

    Candidate Resume :
    {resume.model_dump_json(indent=2)}

    Return valid JSON matching this schema:
    {match_schema}

    Put the following information inside the details object:
    - Candidate name
    - Matching skills
    - Missing important skills
    - Whether the experience requirement is met
    - A short final verdict

    Set score to the overall match percentage from 0 to 100.

                """

    message = {
    "role":"user",
    "content":prompt
    }
    messages= [message ]
    response_format= {
        "type": "json_object"

    }
    response = client.chat.completions.create(
        model= model,
        messages= messages,
        response_format= response_format
    )

    data = json.loads(response.choices[0].message.content)
    return Match_result(**data)

def parse_resume(resume_text):
    if not resume_text or not resume_text.strip():
        raise ValueError("This resume has no extractable text. It may be a scanned PDF.")
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.

    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"
    return text


def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None



# Find an existing resumes folder relative to this script/project.
# For example, this script may be in week1/day5/venv while resumes is in week1/day5/resumes.
script_dir = Path(__file__).resolve().parent
resume_folder = None

for parent in script_dir.parents:
    candidate = parent / "resumes"
    if candidate.is_dir():
        resume_folder = candidate
        break

# If no resumes folder exists yet, create the expected location beside the venv folder.
if resume_folder is None:
    resume_folder = script_dir.parent / "resumes"
    resume_folder.mkdir(parents=True, exist_ok=True)
    raise FileNotFoundError(
        f"No resumes folder with files was found. Created this folder for you:\n"
        f"{resume_folder}\n"
        "Put your .pdf or .docx resume files there, then run the script again."
    )

resume_files = sorted(
    file_path for file_path in resume_folder.iterdir()
    if file_path.is_file() and file_path.suffix.lower() in {".pdf", ".docx"}
)

if not resume_files:
    raise FileNotFoundError(
        f"No PDF or DOCX resumes found in: {resume_folder}\n"
        "Add resume files to this folder and run the script again."
    )

print(f"Using resume folder: {resume_folder}")
all_results = []

for file_path in resume_files:
    print(f"\\nProcessing: {file_path.name}")

    try:
        resume_text = read_resume(file_path)
        parsed_resume = parse_resume(resume_text)
        time.sleep(2)

        result = final_score(job, parsed_resume)
        time.sleep(2)

        # Keep scores in the valid range for reporting.
        score = max(0.0, min(100.0, result.score))
        print(f"Score: {score:.1f}%")

        all_results.append({
            "name": parsed_resume.name or file_path.stem,
            "score": score,
            "details": result.details,
        })

    except Exception as exc:
        print(f"Skipping {file_path.name} because of an error: {exc}")

if not all_results:
    raise RuntimeError(
        "No resumes could be processed successfully. Check the errors printed above."
    )

all_results.sort(key=lambda candidate: candidate["score"], reverse=True)

print("\\nTOP 2 CANDIDATES")
for candidate in all_results[:2]:
    print(f"{candidate['name']} - {candidate['score']:.1f}%")
    print(candidate["details"])

print("\\nLOWEST 2 CANDIDATES")
for candidate in all_results[-2:]:
    print(f"{candidate['name']} - {candidate['score']:.1f}%")
    print(candidate["details"])
