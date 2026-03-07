from __future__ import annotations

from typing import Dict, List

DEFAULT_GENERIC_QUESTIONS = [
    "Explain a recent project where you used this technology and the toughest issue you solved.",
    "What are common performance bottlenecks in this technology, and how do you mitigate them?",
    "How do you test, debug, and maintain code built with this technology in production?",
]

QUESTION_BANK: Dict[str, List[str]] = {
    "python": [
        "What is the difference between a list and a tuple, and when would you choose each?",
        "How does Python's GIL affect concurrency, and what are practical workarounds?",
        "How would you optimize a slow Python data-processing pipeline?",
    ],
    "django": [
        "Explain Django's request-response lifecycle and where middleware fits in.",
        "How do you design secure authentication and authorization in Django?",
        "What strategies do you use to reduce N+1 query issues in Django ORM?",
    ],
    "flask": [
        "How does Flask differ from Django architecturally, and when would you prefer Flask?",
        "How would you structure a medium-sized Flask application for maintainability?",
        "How do you handle configuration and secrets in Flask across environments?",
    ],
    "javascript": [
        "Explain event loop behavior in JavaScript with examples of microtasks vs macrotasks.",
        "What are closures and how have you used them in real projects?",
        "How do you prevent and debug memory leaks in frontend applications?",
    ],
    "react": [
        "How does React reconciliation work and why are stable keys important?",
        "When would you use context, Redux, or local component state?",
        "How do you profile and optimize React rendering performance?",
    ],
    "node.js": [
        "How do you handle CPU-bound workloads in a Node.js service?",
        "Explain middleware patterns in Express and their trade-offs.",
        "How do you design robust error handling and logging in Node.js APIs?",
    ],
    "sql": [
        "What indexing strategy would you use for a high-read table and why?",
        "Explain normalization vs denormalization trade-offs with a practical example.",
        "How do you debug a slow SQL query in production?",
    ],
    "postgresql": [
        "What are PostgreSQL transaction isolation levels and when do they matter?",
        "How would you tune PostgreSQL for write-heavy workloads?",
        "What is VACUUM and why is it important in PostgreSQL?",
    ],
    "mongodb": [
        "How do you decide between embedding and referencing in MongoDB schema design?",
        "What indexing choices would you make for a query-heavy collection?",
        "How do you maintain consistency in a MongoDB-based system?",
    ],
    "aws": [
        "How would you design a scalable and cost-aware web backend on AWS?",
        "What is the difference between security groups and NACLs?",
        "How do you monitor and troubleshoot failures in distributed AWS services?",
    ],
    "docker": [
        "What are common causes of large Docker images and how do you reduce image size?",
        "How do you manage secrets and environment configuration in containerized apps?",
        "How would you debug a container that works locally but fails in deployment?",
    ],
    "kubernetes": [
        "Explain how Deployments, Services, and Ingress work together in Kubernetes.",
        "How do readiness/liveness probes affect rollout stability?",
        "How would you troubleshoot a CrashLoopBackOff in production?",
    ],
    "machine learning": [
        "How do you diagnose overfitting and what mitigation methods do you prefer?",
        "How do you select evaluation metrics for imbalanced classification problems?",
        "Describe your approach to model monitoring after deployment.",
    ],
    "devops": [
        "How would you design a CI/CD pipeline with fast feedback and safe production rollouts?",
        "What is your approach to infrastructure as code, drift detection, and rollback?",
        "How do you define and track SLOs/SLIs for platform reliability?",
    ],
    "mlops": [
        "How do you version datasets, models, and feature pipelines for reproducible ML releases?",
        "What deployment pattern do you prefer for ML models and why?",
        "How do you detect model/data drift and trigger retraining safely?",
    ],
    "sde": [
        "How do you design a scalable service API and choose the right data model?",
        "Explain how you debug a production incident end-to-end.",
        "What trade-offs do you consider between readability, performance, and delivery speed?",
    ],
    "software development engineer": [
        "How do you design a scalable service API and choose the right data model?",
        "Explain how you debug a production incident end-to-end.",
        "What trade-offs do you consider between readability, performance, and delivery speed?",
    ],
    "backend": [
        "How do you design idempotent APIs and handle retries safely?",
        "What caching strategy would you use for mixed read/write workloads?",
        "How do you secure backend services (authn/authz, secrets, and rate limiting)?",
    ],
    "frontend": [
        "How do you optimize Core Web Vitals in a large frontend application?",
        "How do you structure state management across page, feature, and global scopes?",
        "How do you ensure accessibility (a11y) in reusable UI components?",
    ],
    "web designing": [
        "How do you convert a design system into responsive, reusable UI components?",
        "How do you balance visual quality with performance on low-end devices?",
        "How do you validate usability and accessibility before handoff?",
    ],
    "web design": [
        "How do you convert a design system into responsive, reusable UI components?",
        "How do you balance visual quality with performance on low-end devices?",
        "How do you validate usability and accessibility before handoff?",
    ],
    "testing": [
        "How do you define a practical testing pyramid for a web product?",
        "How do you reduce flaky tests in CI while keeping execution time low?",
        "How do you choose between unit, integration, and end-to-end tests for a feature?",
    ],
    "qa": [
        "How do you build a risk-based test plan under tight deadlines?",
        "How do you track defect leakage and improve release quality over time?",
        "How do you automate regression tests without creating brittle suites?",
    ],
    "research": [
        "How do you design experiments and pick meaningful baselines?",
        "How do you ensure your conclusions are statistically and practically valid?",
        "How do you document and reproduce research results for team handoff?",
    ],
    "video editing": [
        "How do you optimize an editing workflow for speed, consistency, and quality?",
        "How do you choose codecs, bitrates, and export settings for different platforms?",
        "How do you manage color, audio leveling, and asset organization at scale?",
    ],
    "fastapi": [
        "How do you structure FastAPI dependencies, routers, and service layers for maintainability?",
        "How do you implement auth, validation, and error handling consistently in FastAPI?",
        "How do you optimize FastAPI performance for high-concurrency workloads?",
    ],
    "rest apis": [
        "How do you version REST APIs without breaking consumers?",
        "How do you design pagination, filtering, and sorting for large datasets?",
        "How do you implement idempotency and error contracts in REST endpoints?",
    ],
    "linux": [
        "How do you investigate sudden CPU, memory, and I/O spikes on a Linux host?",
        "What process and network tools do you use during incident response and why?",
        "How do you harden Linux servers for production workloads?",
    ],
    "git/github": [
        "How do you design a branching and release strategy for multiple parallel features?",
        "How do you handle rebasing/merging conflicts in long-running branches?",
        "How do you enforce code quality checks in pull-request workflows?",
    ],
    "container deployment": [
        "How do you design deployment strategies (blue/green, canary, rolling) for containers?",
        "How do you handle config/secrets and environment parity across stages?",
        "How do you debug network/service discovery failures in containerized apps?",
    ],
    "mysql": [
        "How do you optimize MySQL queries with indexes and execution plan analysis?",
        "How do you handle transactional consistency in high-concurrency MySQL systems?",
        "What backup and replication strategy would you use for MySQL production?",
    ],
    "nosql": [
        "How do you choose between document, key-value, and wide-column NoSQL models?",
        "How do you model data for query patterns in NoSQL systems?",
        "How do you handle consistency and partition tolerance trade-offs in NoSQL?",
    ],
    "azure": [
        "How would you architect a secure, scalable application on Azure?",
        "How do you monitor and control cloud spend in Azure environments?",
        "How do you design identity and access policies in Azure for least privilege?",
    ],
    "gcp": [
        "How would you design a reliable service stack on GCP for global users?",
        "How do you balance cost and performance for GCP compute/storage choices?",
        "How do you set up observability and incident alerting in GCP?",
    ],
    "transformers": [
        "How does attention work in transformer architectures, and why is it effective?",
        "How do you fine-tune transformers efficiently for domain-specific tasks?",
        "How do you evaluate hallucination and factuality in transformer outputs?",
    ],
    "nlp": [
        "How do you design an NLP pipeline from preprocessing to evaluation?",
        "How do you handle class imbalance and noisy labels in NLP tasks?",
        "How do you compare rule-based, classical ML, and transformer NLP approaches?",
    ],
    "rag": [
        "How do you choose chunking strategy and embedding model for a RAG pipeline?",
        "How do you evaluate retrieval quality separately from generation quality?",
        "How do you reduce hallucinations in RAG responses under ambiguous queries?",
    ],
    "langchain": [
        "How do you structure chains/agents and tool-calling with reliability in LangChain?",
        "How do you observe and debug LangChain applications in production?",
        "How do you control prompt/version changes in LangChain workflows?",
    ],
    "model evaluation": [
        "How do you choose offline and online metrics that align with business goals?",
        "How do you design robust evaluation sets to avoid benchmark leakage?",
        "How do you compare models fairly across latency, cost, and quality?",
    ],
    "prompt engineering": [
        "How do you design prompts that are robust to ambiguous user input?",
        "How do you test prompt changes and prevent regressions systematically?",
        "How do you reduce token cost while preserving output quality?",
    ],
    "openai api": [
        "How do you design retries, timeouts, and fallback behavior for LLM API calls?",
        "How do you handle prompt injection and output validation in production?",
        "How do you optimize latency/cost across model and context choices?",
    ],
    "llama": [
        "How do you choose quantization and serving strategy for LLaMA models?",
        "How do you evaluate instruction-following quality after fine-tuning?",
        "How do you deploy and monitor self-hosted LLaMA inference safely?",
    ],
    "tensorflow": [
        "How do you optimize TensorFlow training with data pipelines and mixed precision?",
        "How do you debug shape, gradient, and convergence issues in TensorFlow?",
        "How do you export and serve TensorFlow models reliably?",
    ],
    "pytorch": [
        "How do you structure a PyTorch training loop for reproducibility?",
        "How do you profile GPU bottlenecks in PyTorch workloads?",
        "How do you manage checkpointing and experiment tracking in PyTorch projects?",
    ],
    "pandas": [
        "How do you optimize slow Pandas transformations on large datasets?",
        "How do you detect and handle data quality issues in Pandas pipelines?",
        "How do you design Pandas code for readability and reproducibility?",
    ],
    "numpy": [
        "How does vectorization improve NumPy performance over Python loops?",
        "How do broadcasting rules work, and how do you debug shape mismatches?",
        "How do you manage memory when processing large arrays in NumPy?",
    ],
    "seaborn": [
        "How do you choose the right Seaborn plot for comparing distributions and relationships?",
        "How do you prevent misleading visualizations when data is skewed or imbalanced?",
        "How do you standardize chart styling for stakeholder-facing reports?",
    ],
    "eda/etl": [
        "How do you structure EDA to quickly identify high-impact data issues?",
        "How do you design ETL jobs for idempotency, observability, and recoverability?",
        "How do you validate ETL outputs before downstream consumption?",
    ],
    "tableau": [
        "How do you optimize Tableau dashboards for performance on large data sources?",
        "How do you design actionable dashboards for non-technical stakeholders?",
        "How do you control metric definitions and governance in Tableau projects?",
    ],
    "powerbi": [
        "How do you model data and DAX measures for scalable Power BI reports?",
        "How do you improve refresh performance and report responsiveness in Power BI?",
        "How do you manage row-level security and sharing in Power BI?",
    ],
    "r programming": [
        "How do you organize R analysis scripts for reproducible research?",
        "How do you optimize slow operations in base R vs tidyverse workflows?",
        "How do you package and communicate statistical findings clearly in R?",
    ],
    "java": [
        "How do JVM memory settings and GC choices affect application performance?",
        "How do you design thread-safe components in Java services?",
        "How do you structure Java applications for testability and maintainability?",
    ],
    "c++": [
        "How do you manage memory ownership and lifetime safely in modern C++?",
        "How do you diagnose and optimize CPU/memory hotspots in C++ applications?",
        "How do you design C++ modules to avoid tight coupling and long build times?",
    ],
    "html": [
        "How do semantic HTML choices improve accessibility and SEO?",
        "How do you structure complex page layouts while keeping markup maintainable?",
        "How do you validate and test HTML for cross-browser consistency?",
    ],
    "css": [
        "How do you design scalable CSS architecture for large codebases?",
        "How do you handle responsive design across breakpoints and device classes?",
        "How do you debug specificity and cascade issues efficiently?",
    ],
    "figma": [
        "How do you create reusable component libraries and variants in Figma?",
        "How do you manage design handoff to developers with minimal ambiguity?",
        "How do you run design critique and iteration cycles effectively?",
    ],
    "webflow": [
        "How do you structure reusable components and CMS collections in Webflow?",
        "How do you optimize Webflow pages for performance and SEO?",
        "How do you manage responsive interactions and animations without harming UX?",
    ],
    "testing automation": [
        "How do you prioritize automation candidates from a large manual test suite?",
        "How do you design maintainable automation frameworks for long-term use?",
        "How do you integrate automation results into release-go/no-go decisions?",
    ],
    "selenium": [
        "How do you design Selenium tests to reduce flakiness in dynamic UIs?",
        "How do you structure page objects and fixtures for maintainable Selenium suites?",
        "How do you parallelize Selenium execution in CI efficiently?",
    ],
    "pytest": [
        "How do you use fixtures and parametrization to keep test code DRY?",
        "How do you balance unit vs integration tests in a Python codebase?",
        "How do you speed up pytest runs in CI pipelines?",
    ],
    "playwright": [
        "How do you use Playwright tracing and network mocking for reliable E2E tests?",
        "How do you design resilient selectors and avoid brittle UI tests?",
        "How do you run Playwright suites across browsers at scale?",
    ],
    "cypress": [
        "How do you organize Cypress tests for fast and stable CI execution?",
        "How do you handle API stubbing and state setup in Cypress?",
        "How do you debug flaky Cypress tests and reduce reruns?",
    ],
    "jenkins": [
        "How do you design Jenkins pipelines for secure, multi-environment deployments?",
        "How do you manage shared libraries and pipeline reuse in Jenkins?",
        "How do you handle secrets and credential rotation in Jenkins jobs?",
    ],
    "github actions": [
        "How do you design reusable GitHub Actions workflows for multiple repositories?",
        "How do you optimize workflow runtime and caching strategy in GitHub Actions?",
        "How do you secure CI workflows against supply-chain and secret leakage risks?",
    ],
    "terraform": [
        "How do you structure Terraform modules for reuse and environment isolation?",
        "How do you manage Terraform state securely in team settings?",
        "How do you handle safe plan/apply workflows in CI/CD?",
    ],
    "prometheus": [
        "How do you design Prometheus metrics to avoid high-cardinality issues?",
        "How do you create alert rules that are actionable and low-noise?",
        "How do you troubleshoot missing or inaccurate telemetry in Prometheus?",
    ],
    "grafana": [
        "How do you design Grafana dashboards that support incident triage?",
        "How do you standardize dashboard templates across services?",
        "How do you connect Grafana alerts to escalation workflows effectively?",
    ],
    "airflow": [
        "How do you design Airflow DAGs for idempotency and failure recovery?",
        "How do you tune scheduler/executor settings for large DAG volumes?",
        "How do you monitor and debug delayed or stuck Airflow tasks?",
    ],
    "mlflow": [
        "How do you organize experiment tracking and model registry in MLflow?",
        "How do you enforce promotion criteria from staging to production models?",
        "How do you connect MLflow artifacts with CI/CD release workflows?",
    ],
    "dvc": [
        "How do you version large datasets and pipelines effectively with DVC?",
        "How do you set up remote storage and collaboration workflows in DVC?",
        "How do you reproduce historical experiments end-to-end using DVC?",
    ],
    "kubeflow": [
        "How do you design Kubeflow pipelines for reproducible training workflows?",
        "How do you manage model serving and rollout policies with Kubeflow?",
        "How do you monitor resource usage and failures in Kubeflow jobs?",
    ],
}


def questions_for_tech(tech: str) -> List[str]:
    key = tech.strip().lower()
    return QUESTION_BANK.get(key, DEFAULT_GENERIC_QUESTIONS)
