"""
resume_parser.py — 100% local, zero API calls
─────────────────────────────────────────────
1. Extract raw text from PDF or image bytes
2. Parse keywords: skills, companies, projects, education, years
3. Generate personalised interview questions from templates
"""

import io
import re
from collections import defaultdict


# ─────────────────────────────────────────────────────────────────────────────
# TECH KEYWORD DICTIONARY  (grouped by category for question selection)
# ─────────────────────────────────────────────────────────────────────────────
TECH_GROUPS = {
    "Python":       ["python", "django", "flask", "fastapi", "celery", "pandas", "numpy", "scipy"],
    "JavaScript":   ["javascript", "js", "typescript", "ts", "node", "nodejs", "express", "nestjs"],
    "React":        ["react", "reactjs", "react.js", "redux", "next.js", "nextjs", "gatsby"],
    "Vue":          ["vue", "vuejs", "vue.js", "nuxt"],
    "Angular":      ["angular", "angularjs"],
    "Java":         ["java", "spring", "springboot", "spring boot", "hibernate", "maven", "gradle"],
    "Kotlin":       ["kotlin", "android"],
    "Swift":        ["swift", "ios", "xcode", "swiftui"],
    "Go":           ["golang", "go lang", " go "],
    "Rust":         ["rust", "cargo"],
    "C++":          ["c++", "cpp", "c plus plus"],
    "C#":           ["c#", "dotnet", ".net", "asp.net", "csharp"],
    "Ruby":         ["ruby", "rails", "ruby on rails"],
    "PHP":          ["php", "laravel", "symfony", "wordpress"],
    "Scala":        ["scala", "akka", "play framework"],
    "R":            [" r ", "rstudio", "tidyverse", "ggplot"],
    "SQL":          ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle db", "mssql", "t-sql"],
    "MongoDB":      ["mongodb", "mongo", "mongoose"],
    "Redis":        ["redis", "redis cache"],
    "Elasticsearch":["elasticsearch", "elastic", "kibana", "logstash", "elk"],
    "Cassandra":    ["cassandra", "apache cassandra"],
    "DynamoDB":     ["dynamodb", "dynamo"],
    "GraphQL":      ["graphql", "apollo"],
    "REST":         ["rest api", "restful", "rest ful"],
    "gRPC":         ["grpc", "protobuf", "protocol buffer"],
    "Docker":       ["docker", "dockerfile", "docker-compose", "docker compose"],
    "Kubernetes":   ["kubernetes", "k8s", "kubectl", "helm", "eks", "gke", "aks"],
    "AWS":          ["aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudwatch", "iam", "vpc", "ecs", "eks"],
    "GCP":          ["gcp", "google cloud", "bigquery", "cloud run", "gke", "pubsub"],
    "Azure":        ["azure", "microsoft azure", "aks", "azure functions"],
    "Terraform":    ["terraform", "infrastructure as code", "iac"],
    "CI/CD":        ["ci/cd", "jenkins", "github actions", "gitlab ci", "circleci", "travis"],
    "Kafka":        ["kafka", "apache kafka", "event streaming"],
    "RabbitMQ":     ["rabbitmq", "amqp", "message queue"],
    "Linux":        ["linux", "ubuntu", "centos", "bash", "shell script"],
    "Git":          ["git", "github", "gitlab", "bitbucket"],
    "Machine Learning": ["machine learning", "ml", "scikit-learn", "sklearn", "xgboost", "lightgbm"],
    "Deep Learning":["deep learning", "tensorflow", "keras", "pytorch", "neural network", "cnn", "rnn", "lstm", "transformer"],
    "NLP":          ["nlp", "natural language processing", "bert", "gpt", "huggingface", "spacy", "nltk"],
    "Data Engineering": ["spark", "apache spark", "pyspark", "airflow", "dbt", "data pipeline", "etl", "elt"],
    "Microservices":["microservice", "microservices", "service mesh", "istio"],
    "Blockchain":   ["blockchain", "solidity", "ethereum", "smart contract", "web3"],
}

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION TEMPLATES  keyed by tech group
# ─────────────────────────────────────────────────────────────────────────────
TECH_QUESTIONS = {
    "Python": [
        "Your résumé mentions Python — explain how the GIL affects concurrency and when you'd use multiprocessing vs asyncio.",
        "Walk me through how you've used Python decorators or context managers in a real project.",
        "Describe a memory management challenge you faced in a Python service and how you resolved it.",
    ],
    "JavaScript": [
        "Explain the event loop and how you've handled async operations in your JavaScript projects.",
        "Describe a closure or prototype chain issue you debugged in production.",
        "How have you managed state or side-effects in a large JavaScript codebase?",
    ],
    "React": [
        "In your React work, when did you choose useCallback vs useMemo, and what was the trade-off?",
        "Describe a performance bottleneck you hit in a React app and how you diagnosed it.",
        "How have you structured component re-renders and state management in a large React project?",
    ],
    "Java": [
        "Explain how you've used Java's thread pool and where you saw contention issues.",
        "Describe a Spring Boot microservice you built — what design patterns did you use?",
        "How have you handled JVM memory tuning (GC, heap sizing) in a production service?",
    ],
    "Go": [
        "Describe how you've used goroutines and channels to solve a concurrency problem.",
        "How did you handle error propagation and retries in a Go service you built?",
        "What made you choose Go for a project, and what limitations did you hit?",
    ],
    "SQL": [
        "Describe a slow SQL query you diagnosed and how you optimised it.",
        "Walk me through your indexing strategy for a high-traffic table you've worked on.",
        "How have you handled schema migrations in a production database with zero downtime?",
    ],
    "MongoDB": [
        "When have you chosen MongoDB over relational DB, and what schema design did you use?",
        "Describe an aggregation pipeline you built and the performance trade-offs.",
        "How did you handle data consistency in a MongoDB sharded cluster?",
    ],
    "Docker": [
        "Walk me through your Dockerfile optimisation strategy for faster builds.",
        "Describe a multi-container setup you built with Docker Compose — what challenges came up?",
        "How have you handled secrets and environment config in Docker deployments?",
    ],
    "Kubernetes": [
        "Describe a Kubernetes deployment issue you debugged — pods crashing, OOMKilled, etc.",
        "How have you configured resource limits, autoscaling, and health probes in your clusters?",
        "Walk me through your strategy for zero-downtime deployments in Kubernetes.",
    ],
    "AWS": [
        "Describe an AWS architecture you designed — what services did you choose and why?",
        "How have you handled IAM roles and least-privilege access in an AWS project?",
        "Walk me through a cost optimisation you did on AWS infrastructure.",
    ],
    "Machine Learning": [
        "Describe an end-to-end ML pipeline you built — data prep, training, evaluation, deployment.",
        "How did you handle class imbalance or data quality issues in a real project?",
        "Walk me through a model that underperformed — how did you debug and improve it?",
    ],
    "Deep Learning": [
        "Describe a neural network architecture you designed — why those layers and hyperparameters?",
        "How have you handled overfitting in a deep learning model you trained?",
        "Walk me through your GPU training setup and how you optimised throughput.",
    ],
    "Kafka": [
        "Describe a Kafka-based architecture you built — what partitioning strategy did you use?",
        "How did you handle consumer lag and message ordering guarantees in your system?",
        "Walk me through a failure scenario in your Kafka setup and how you recovered.",
    ],
    "Microservices": [
        "How did you handle inter-service communication and failure isolation in your microservices?",
        "Describe the biggest challenge you faced breaking a monolith into microservices.",
        "How have you implemented distributed tracing or observability across your services?",
    ],
    "CI/CD": [
        "Walk me through a CI/CD pipeline you built from scratch — what stages and gates did it have?",
        "Describe a deployment that went wrong in your pipeline and how you rolled back.",
        "How did you implement environment-specific config and secrets in your pipeline?",
    ],
    "default": [
        "Describe a challenging technical problem you solved using {tech} in a real project.",
        "Walk me through the most complex feature you built using {tech}.",
        "What limitations or trade-offs did you encounter with {tech} in production?",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION PATTERNS
# ─────────────────────────────────────────────────────────────────────────────
_PROJECT_PATTERNS = re.compile(
    r'(?:project|built|developed|created|implemented|designed|architected|launched|deployed)\s+'
    r'(?:a\s+|an\s+|the\s+)?([A-Z][A-Za-z0-9\s\-_]{3,50})',
    re.IGNORECASE
)
_COMPANY_PATTERNS = re.compile(
    r'(?:at|@|with|for|worked at|employed at|joined)\s+([A-Z][A-Za-z0-9\s&.,\-]{2,40})'
    r'(?:\s+as|\s+where|\s+from|\s+\(|,|\.|$)',
    re.IGNORECASE
)
_YEAR_PATTERN = re.compile(r'\b(20\d{2})\b')
_EXP_PATTERN  = re.compile(
    r'(\d+\.?\d*)\s*\+?\s*(?:years?|yrs?)(?:\s+of)?\s*(?:experience|exp)?',
    re.IGNORECASE
)
_SECTION_HEADERS = re.compile(
    r'^(?:experience|work experience|projects?|education|skills?|'
    r'technical skills?|certifications?|achievements?|summary|objective)\s*$',
    re.IGNORECASE | re.MULTILINE
)


# ─────────────────────────────────────────────────────────────────────────────
# PDF / IMAGE TEXT EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF using two libraries for maximum coverage.
    1. pdfplumber  — better at complex layouts, tables, multi-column
    2. pypdf       — fallback for simpler PDFs
    Zero API calls.
    """
    text = ""

    # Method 1: pdfplumber (handles most modern resume PDFs)
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = []
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    pages.append(t.strip())
            text = "\n\n".join(pages)
    except Exception:
        pass

    # Method 2: pypdf fallback
    if not text.strip():
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = []
            for page in reader.pages:
                t = page.extract_text()
                if t and t.strip():
                    pages.append(t.strip())
            text = "\n\n".join(pages)
        except Exception:
            pass

    return text[:15000]  # cap at ~4k tokens


def extract_text_from_image(file_bytes: bytes) -> str:
    """
    For image resumes we can't do local OCR without heavy deps.
    Return a sentinel so caller can show a helpful message.
    """
    return "__IMAGE__"


# ─────────────────────────────────────────────────────────────────────────────
# KEYWORD EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────
def extract_skills(text: str) -> list[str]:
    """Find all tech skills mentioned in the resume text."""
    text_lower = text.lower()
    found = []
    for group_name, keywords in TECH_GROUPS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(group_name)
                break
    return list(dict.fromkeys(found))   # deduplicated, order preserved


def extract_companies(text: str) -> list[str]:
    """
    Extract company names from résumé.
    Strategy: look for lines matching "Role at Company | Date" patterns.
    """
    companies = []
    seen = set()

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # Pattern: "Role at CompanyName | date" or "CompanyName | Role | date"
        at_match = re.search(r'\bat\s+([A-Z][A-Za-z0-9\s&.\-]{2,35})\s*[|,]', stripped)
        if at_match:
            name = at_match.group(1).strip()
            if name.lower() not in seen and len(name) > 2:
                seen.add(name.lower())
                companies.append(name)
                continue

        # Pattern: line has year range and a pipe — likely "Company | Role | 2020-2022"
        if re.search(r'20\d{2}', stripped) and '|' in stripped:
            parts = [p.strip() for p in stripped.split("|")]
            # First part is often company or role — pick the one that looks like a proper noun
            for part in parts[:2]:
                part = part.strip()
                if (len(part) > 2 and len(part) < 40
                        and part[0].isupper()
                        and not re.search(r'\d{4}', part)          # not a date
                        and part.lower() not in seen):
                    seen.add(part.lower())
                    companies.append(part)
                    break

    return companies[:5]


def extract_projects(text: str) -> list[str]:
    """
    Extract project titles from the Projects section of a résumé.
    Returns only clean titles (short lines, not bullet-point descriptions).
    """
    projects = []
    in_projects = False
    bullet = re.compile(r'^[-•*▪◦]\s*')

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # Detect section header
        if re.match(r'^projects?\s*$', stripped, re.IGNORECASE):
            in_projects = True
            continue
        if re.match(
            r'^(?:experience|work experience|education|skills|certifications?|'
            r'achievements?|summary|objective|contact|profile)\s*$',
            stripped, re.IGNORECASE
        ):
            in_projects = False
            continue

        if in_projects:
            # Skip bullet points (descriptions)
            if bullet.match(stripped):
                continue
            # Short lines (10–60 chars) that look like titles, not dates or emails
            if (10 < len(stripped) < 60
                    and not re.search(r'20\d{2}', stripped)
                    and not re.search(r'@|http|www', stripped)
                    and not stripped.endswith(":")):
                # Avoid duplicate / very similar titles
                if not any(p.lower() in stripped.lower() or stripped.lower() in p.lower()
                           for p in projects):
                    projects.append(stripped)

    return projects[:4]



def extract_experience_years(text: str) -> str:
    """Extract years of experience if mentioned."""
    m = _EXP_PATTERN.search(text)
    if m:
        return f"{m.group(1)} years"
    # Count year range spans
    years = sorted(set(int(y) for y in _YEAR_PATTERN.findall(text)))
    if len(years) >= 2:
        span = years[-1] - years[0]
        if 1 <= span <= 30:
            return f"~{span} years"
    return ""


def extract_education(text: str) -> str:
    """Extract highest degree and institution."""
    degrees = ["ph.d", "phd", "m.tech", "m.s.", "msc", "m.e.", "mba",
               "b.tech", "b.e.", "bsc", "b.s.", "bachelor", "master", "doctor"]
    text_lower = text.lower()
    for line in text.split("\n"):
        ll = line.lower().strip()
        if any(d in ll for d in degrees) and len(line.strip()) > 5:
            return line.strip()[:100]
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# QUESTION GENERATION  (100% template-based, zero API)
# ─────────────────────────────────────────────────────────────────────────────
def generate_resume_questions(
    skills: list[str],
    projects: list[str],
    companies: list[str],
    experience: str,
    raw_text: str,
) -> list[dict]:
    """
    Generate up to 5 personalised questions.
    Returns list of dicts: {question, category, source}
    """
    questions = []

    # ── 1. Project-based questions (most personal) ──────────────────────────
    for proj in projects[:2]:
        title = proj if len(proj) <= 45 else proj[:42] + "…"
        q = {
            "question": f"Your résumé mentions **{title}** — walk me through the most challenging part of building it and what you'd do differently now.",
            "category": "project",
            "source":   title,
        }
        questions.append(q)

    # ── 2. Experience / company questions ───────────────────────────────────
    if companies:
        co = companies[0]
        questions.append({
            "question": f"At **{co}**, what was the most technically complex problem you solved, and what was your approach?",
            "category": "experience",
            "source":   co,
        })

    if len(companies) >= 2:
        co1, co2 = companies[0], companies[1]
        questions.append({
            "question": f"You've worked at both **{co1}** and **{co2}** — what was the biggest technical or architectural difference between the two environments?",
            "category": "experience",
            "source":   f"{co1} / {co2}",
        })

    # ── 3. Skill-depth questions ────────────────────────────────────────────
    used_groups = set()
    for skill in skills:
        if len(questions) >= 5:
            break
        if skill in used_groups:
            continue
        used_groups.add(skill)
        pool = TECH_QUESTIONS.get(skill, [])
        if pool:
            questions.append({
                "question": pool[len(questions) % len(pool)],
                "category": "technical",
                "source":   skill,
            })
        else:
            # Use default template
            tmpl = TECH_QUESTIONS["default"][0].replace("{tech}", skill)
            questions.append({
                "question": tmpl,
                "category": "technical",
                "source":   skill,
            })

    # Deduplicate and cap at 5
    seen = set()
    final = []
    for q in questions:
        if q["question"] not in seen:
            seen.add(q["question"])
            final.append(q)
        if len(final) == 5:
            break

    return final


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def parse_resume(file_bytes: bytes, mime_type: str) -> dict:
    """
    Full local resume parsing pipeline. Zero API calls.

    Returns:
    {
      "text":       raw extracted text,
      "skills":     [...],
      "companies":  [...],
      "projects":   [...],
      "education":  "...",
      "experience": "...",
      "questions":  [{question, category, source}, ...],
      "is_image":   bool,
      "error":      str or None,
    }
    """
    result = {
        "text": "", "skills": [], "companies": [], "projects": [],
        "education": "", "experience": "", "questions": [],
        "is_image": False, "error": None,
    }

    # Extract text
    if mime_type == "application/pdf":
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            # Scanned/image PDF - can't extract locally, auto-continue gracefully
            result["error"] = "scanned_pdf"
            return result
    else:
        result["is_image"] = True
        result["error"] = "image_file"
        return result

    result["text"]       = text
    result["skills"]     = extract_skills(text)
    result["companies"]  = extract_companies(text)
    result["projects"]   = extract_projects(text)
    result["education"]  = extract_education(text)
    result["experience"] = extract_experience_years(text)
    result["questions"]  = generate_resume_questions(
        result["skills"],
        result["projects"],
        result["companies"],
        result["experience"],
        text,
    )
    return result