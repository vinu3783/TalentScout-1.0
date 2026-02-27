"""
question_bank.py
─────────────────
Curated real interview questions organized by tech stack and experience level.

Structure:
  QUESTIONS = {
      "technology_key": {
          "fresher": [...],   # 0-2 yrs — conceptual + basic practical
          "experienced": [...] # 3+ yrs — internals, trade-offs, production scenarios
      }
  }

Usage:
  from question_bank import get_questions_for_stack
  questions = get_questions_for_stack(["Python", "Django", "PostgreSQL"], experience_years=2)
"""

import random
import re

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION BANK
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS = {

    # ── Python ────────────────────────────────────────────────────────────────
    "python": {
        "fresher": [
            "What is the difference between a list and a tuple in Python, and when would you use each?",
            "Explain how Python's garbage collection works and what reference counting means.",
            "What are *args and **kwargs, and how do they differ?",
            "What is a Python decorator and can you write a simple one from scratch?",
            "What is the difference between deep copy and shallow copy in Python?",
            "How does Python handle exceptions — what is the difference between except, else, and finally?",
            "What are list comprehensions and how are they different from map() and filter()?",
            "What is the difference between is and == in Python?",
            "What is a lambda function and when would you use one?",
            "Explain the concept of mutable vs immutable objects in Python with examples.",
        ],
        "experienced": [
            "How does Python's GIL affect CPU-bound vs I/O-bound multithreading, and when would you choose multiprocessing instead?",
            "Explain Python's memory model — how are objects stored, and what is the impact of interning?",
            "How do Python generators and coroutines differ, and when would you use asyncio over threading?",
            "What are Python metaclasses and can you give a real-world use case where you would need one?",
            "How does Python's descriptor protocol work, and how is it used internally by @property?",
            "Explain the MRO (Method Resolution Order) in Python's multiple inheritance — how does C3 linearization work?",
            "What are the trade-offs between using slots and a regular dict for object attribute storage in Python?",
            "How would you profile a Python application that has unexpected memory growth in production?",
            "Describe a time you optimised a Python function from O(n²) to O(n) — what data structures did you use?",
            "How does Python's asyncio event loop work under the hood, and what is the difference between a coroutine and a future?",
        ],
    },

    # ── JavaScript ────────────────────────────────────────────────────────────
    "javascript": {
        "fresher": [
            "What is the difference between var, let, and const in JavaScript?",
            "Explain what a Promise is and how it differs from a callback.",
            "What is event bubbling and event capturing in the DOM?",
            "What does 'this' refer to in different contexts in JavaScript?",
            "What is the difference between == and === in JavaScript?",
            "Explain what closures are in JavaScript with a simple example.",
            "What is the difference between null and undefined?",
            "How does the JavaScript event loop work at a high level?",
            "What are arrow functions and how do they differ from regular functions?",
            "What is destructuring in JavaScript and how do you use it with objects and arrays?",
        ],
        "experienced": [
            "Explain the JavaScript event loop, call stack, microtask queue, and macrotask queue — in what order do they execute?",
            "How does prototypal inheritance work in JavaScript, and how does it differ from classical inheritance?",
            "What are WeakMap and WeakSet, and when would you use them over Map and Set?",
            "How does JavaScript's memory management work, and how would you identify a memory leak in a long-running browser app?",
            "Explain the difference between throttling and debouncing — implement one from scratch.",
            "What are JavaScript Proxies and Reflect, and give a real use case for them?",
            "How does tree-shaking work in module bundlers, and what code patterns prevent it from working?",
            "Explain how async/await works under the hood in terms of generators and Promises.",
            "What are the performance implications of using closures in hot code paths?",
            "How would you design a client-side caching layer for API responses in a large SPA?",
        ],
    },

    # ── React ─────────────────────────────────────────────────────────────────
    "react": {
        "fresher": [
            "What is the difference between state and props in React?",
            "What is the virtual DOM and why does React use it?",
            "When would you use useEffect and what does the dependency array do?",
            "What is the difference between a controlled and an uncontrolled component?",
            "What is JSX and how does it get converted to JavaScript?",
            "What are React keys and why are they important in lists?",
            "What is the difference between class components and functional components?",
            "What does useState return and how do you update an object in state correctly?",
            "What is prop drilling and how can Context API help solve it?",
            "Explain the component lifecycle — when does a component mount, update, and unmount?",
        ],
        "experienced": [
            "What is the difference between useCallback and useMemo — give a scenario where confusing them causes a bug?",
            "How does React's reconciliation algorithm (Fiber) decide what to re-render, and how can you optimise it?",
            "Explain the trade-offs between Context API and a state management library like Redux or Zustand.",
            "How does React's concurrent mode and Suspense affect rendering, and what problems do they solve?",
            "What are React Server Components, and how do they differ from traditional server-side rendering?",
            "How would you prevent unnecessary re-renders in a component that receives a new object reference as a prop each render?",
            "Explain the rules of hooks — why can't you call hooks inside conditions, and what happens internally if you do?",
            "How would you implement code splitting and lazy loading in a large React application?",
            "Describe how you would architect a React app that needs to share state between deeply nested, unrelated components.",
            "What are the performance trade-offs of using Redux with many small selectors vs. one large selector?",
        ],
    },

    # ── Node.js ───────────────────────────────────────────────────────────────
    "nodejs": {
        "fresher": [
            "What is Node.js and why is it described as non-blocking and event-driven?",
            "What is the difference between require() and ES module import in Node.js?",
            "How does Node.js handle asynchronous operations with the event loop?",
            "What is the purpose of package.json and what is the difference between dependencies and devDependencies?",
            "How do you read and write files asynchronously in Node.js?",
            "What is middleware in Express.js and how does it work?",
            "What is the difference between process.nextTick() and setImmediate()?",
            "How do you handle errors in async/await in a Node.js Express route?",
            "What are streams in Node.js and when would you use them?",
            "What is the difference between npm and npx?",
        ],
        "experienced": [
            "How does the Node.js cluster module work, and when would you use it over a load balancer?",
            "Explain Node.js streams in detail — what are the differences between Readable, Writable, Transform, and Duplex streams?",
            "How would you debug a memory leak in a Node.js production service?",
            "What are worker threads in Node.js and how do they differ from child processes?",
            "How does Node.js handle CPU-intensive tasks without blocking the event loop?",
            "Explain how you would implement rate limiting and request throttling in an Express API.",
            "What is the V8 engine's garbage collector and how does it affect Node.js performance?",
            "How would you structure a large Node.js application for maintainability and testability?",
            "Describe how you would implement graceful shutdown in a Node.js HTTP server.",
            "What are the trade-offs between using callbacks, Promises, and async/await for async control flow in Node.js?",
        ],
    },

    # ── Django ────────────────────────────────────────────────────────────────
    "django": {
        "fresher": [
            "What is the Django MTV pattern and how does it differ from MVC?",
            "What is the difference between a Django model and a database table?",
            "What are Django migrations and why are they important?",
            "What is the Django ORM and how do you perform a basic query with it?",
            "What is the difference between Django's ForeignKey, OneToOneField, and ManyToManyField?",
            "What is a Django view and what is the difference between a function-based and class-based view?",
            "What is Django's settings.py used for and what is the difference between DEBUG=True and DEBUG=False?",
            "What is Django's admin interface and how do you register a model with it?",
            "What is CSRF protection in Django and why is it important?",
            "What are Django template tags and filters — give two examples of each?",
        ],
        "experienced": [
            "How would you optimise a Django view that is making N+1 database queries — what ORM methods would you use?",
            "Explain the Django request/response lifecycle from URL routing to middleware to view to response.",
            "What is select_related vs prefetch_related and when does each one generate a JOIN vs a separate query?",
            "How would you implement caching in a Django application — what backends would you use and at what level?",
            "Explain Django's transaction.atomic() — when would a nested transaction not roll back as expected?",
            "How do you handle database schema changes in production Django with zero downtime?",
            "What is Django Channels and when would you use it over a standard HTTP request/response cycle?",
            "How would you design a multi-tenant Django application where each tenant has isolated data?",
            "Explain Django's content types framework and give a real use case for it.",
            "What are Django signals — when would you use them and what are the risks of overusing them?",
        ],
    },

    # ── FastAPI ───────────────────────────────────────────────────────────────
    "fastapi": {
        "fresher": [
            "What is FastAPI and what advantages does it have over Flask or Django for APIs?",
            "How do you define path parameters and query parameters in a FastAPI route?",
            "What is Pydantic and how does FastAPI use it for request validation?",
            "What is the difference between async def and def in a FastAPI route — when should you use each?",
            "How do you return a custom HTTP status code and response body in FastAPI?",
            "What is dependency injection in FastAPI and how does it work with Depends()?",
            "How do you handle file uploads in FastAPI?",
            "What is OpenAPI and how does FastAPI auto-generate documentation from it?",
            "How do you add CORS middleware to a FastAPI application?",
            "What is the purpose of a FastAPI Router and how do you use it to organise routes?",
        ],
        "experienced": [
            "How does FastAPI's dependency injection system work at a deeper level — how are dependencies resolved and cached?",
            "What is the difference between using a sync database driver and an async driver like asyncpg with FastAPI?",
            "How would you implement background tasks in FastAPI — when would you use BackgroundTasks vs Celery?",
            "Explain how FastAPI handles request lifecycle — middleware, dependencies, route handler, response middleware.",
            "How would you implement JWT authentication with refresh token rotation in FastAPI?",
            "What are the trade-offs between using Pydantic v1 and v2 in a large FastAPI project?",
            "How would you implement rate limiting per user in a FastAPI application without a reverse proxy?",
            "Describe how you would structure a large FastAPI project with multiple domains and shared services.",
            "How does FastAPI's WebSocket support work and what are its limitations vs a dedicated WebSocket server?",
            "How would you write integration tests for a FastAPI application that uses a real database?",
        ],
    },

    # ── Flask ─────────────────────────────────────────────────────────────────
    "flask": {
        "fresher": [
            "What is Flask and how does it differ from Django in terms of philosophy?",
            "How do you define a route in Flask and what HTTP methods does it support?",
            "What is the Flask application context and request context?",
            "How do you use Flask-SQLAlchemy to define a model and query the database?",
            "What is Jinja2 and how does Flask use it for templating?",
            "What is the difference between redirect() and url_for() in Flask?",
            "How do you handle form data and JSON in a Flask POST request?",
            "What is a Blueprint in Flask and why would you use one?",
            "How do you configure Flask for different environments (development, production)?",
            "What is Flask-Login and how does session management work in Flask?",
        ],
        "experienced": [
            "How does Flask's application factory pattern work and why is it better than a global app instance?",
            "How would you implement request-level database connection pooling in Flask with SQLAlchemy?",
            "What are Flask signals and how do they differ from Django signals?",
            "How would you implement background task processing in a Flask application?",
            "Explain the trade-offs between Flask and FastAPI for building a high-throughput REST API.",
            "How would you structure a large Flask application to avoid circular imports?",
            "How do you write unit tests for Flask views that use database sessions?",
            "What is Flask-Migrate and how does it handle Alembic migrations under the hood?",
            "How would you add rate limiting and API key authentication to a Flask REST API?",
            "How does Flask's context locals (g, request, session) work internally with thread-local storage?",
        ],
    },

    # ── PostgreSQL ────────────────────────────────────────────────────────────
    "postgresql": {
        "fresher": [
            "What is the difference between a primary key and a unique constraint in PostgreSQL?",
            "What are indexes in PostgreSQL and when should you add one to a column?",
            "What is the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN?",
            "What is a transaction in PostgreSQL and what does COMMIT and ROLLBACK do?",
            "What is the difference between WHERE and HAVING in a SQL query?",
            "What is a foreign key and how does it enforce referential integrity?",
            "What is the difference between GROUP BY and ORDER BY?",
            "What are NULL values in SQL and why should you be careful with them in comparisons?",
            "What is a subquery and when would you use it instead of a JOIN?",
            "What is the difference between TRUNCATE and DELETE in PostgreSQL?",
        ],
        "experienced": [
            "How would you diagnose a slow PostgreSQL query — which tools and EXPLAIN output fields would you look at?",
            "What is the difference between a B-tree, GIN, GiST, and BRIN index — when would you use each?",
            "How does PostgreSQL MVCC (Multi-Version Concurrency Control) work and what causes table bloat?",
            "What is the difference between SERIALIZABLE, REPEATABLE READ, READ COMMITTED isolation levels in PostgreSQL?",
            "How would you implement a row-level locking strategy to avoid deadlocks in a high-concurrency application?",
            "Explain the difference between a materialised view and a regular view — when would you refresh one?",
            "How does PostgreSQL vacuum work and what happens if autovacuum is not keeping up with your workload?",
            "How would you partition a large PostgreSQL table — what partitioning strategies exist and when would you use each?",
            "Explain how you would implement full-text search in PostgreSQL using tsvector and tsquery.",
            "How would you design a PostgreSQL schema for a multi-tenant SaaS application with row-level security?",
        ],
    },

    # ── MySQL ─────────────────────────────────────────────────────────────────
    "mysql": {
        "fresher": [
            "What is the difference between MyISAM and InnoDB storage engines in MySQL?",
            "What is an index in MySQL and how does it speed up queries?",
            "What is the difference between CHAR and VARCHAR in MySQL?",
            "How do transactions work in MySQL with InnoDB?",
            "What is the difference between UNION and UNION ALL?",
            "What is AUTO_INCREMENT and how does it work in MySQL?",
            "What is the difference between a stored procedure and a function in MySQL?",
            "How does MySQL handle NULL values in indexes?",
            "What are the different types of JOINs in MySQL?",
            "What is the purpose of the EXPLAIN keyword in MySQL?",
        ],
        "experienced": [
            "How does MySQL's InnoDB buffer pool work and how would you tune it for a write-heavy workload?",
            "Explain MySQL replication — what is the difference between statement-based, row-based, and mixed replication?",
            "How would you set up read replicas in MySQL and what are the consistency trade-offs?",
            "What is the difference between optimistic and pessimistic locking in MySQL — when would you use each?",
            "How does MySQL handle deadlocks and what steps would you take to reduce them?",
            "What is MySQL's query cache and why was it removed in MySQL 8.0?",
            "How would you diagnose and fix a slow query in MySQL on a table with millions of rows?",
            "Explain the difference between covering indexes and composite indexes in MySQL.",
            "How does MySQL's MVCC implementation differ from PostgreSQL's?",
            "What is MySQL Group Replication and how does it differ from standard master-slave replication?",
        ],
    },

    # ── MongoDB ───────────────────────────────────────────────────────────────
    "mongodb": {
        "fresher": [
            "What is MongoDB and how does it differ from a relational database?",
            "What is a document in MongoDB and what format does it use?",
            "What is the difference between find() and findOne() in MongoDB?",
            "What are MongoDB collections and how do they differ from SQL tables?",
            "How do you create an index in MongoDB and why is it important?",
            "What is the _id field in MongoDB and what is its default type?",
            "What is the difference between $set and $replace in a MongoDB update?",
            "What is an aggregation pipeline in MongoDB at a basic level?",
            "How do you handle relationships between documents in MongoDB — embedding vs referencing?",
            "What is a MongoDB replica set and why would you use one?",
        ],
        "experienced": [
            "How does MongoDB's WiredTiger storage engine handle concurrency and what is its locking model?",
            "Explain the MongoDB aggregation pipeline — build a pipeline that groups orders by customer and computes revenue.",
            "What is the difference between a MongoDB replica set and a sharded cluster — when do you need sharding?",
            "How does MongoDB handle transactions across multiple documents — what are the limitations?",
            "How would you design a MongoDB schema for a social media feed that needs to be paginated efficiently?",
            "What is a covered query in MongoDB and how do you design an index to enable it?",
            "How does MongoDB's change streams feature work and what are its use cases?",
            "What is the oplog in MongoDB and how is it used by replica sets?",
            "How would you debug a slow MongoDB query — what tools and indexes would you consider?",
            "What are the trade-offs of embedding documents vs. referencing in a write-heavy MongoDB application?",
        ],
    },

    # ── Docker ────────────────────────────────────────────────────────────────
    "docker": {
        "fresher": [
            "What is Docker and how does it differ from a virtual machine?",
            "What is a Dockerfile and what do the instructions FROM, RUN, COPY, and CMD do?",
            "What is the difference between a Docker image and a Docker container?",
            "What is Docker Compose and when would you use it?",
            "How do you expose a port from a Docker container to the host?",
            "What is a Docker volume and why do you need it for persistent data?",
            "What does docker ps and docker logs do?",
            "What is the difference between ENTRYPOINT and CMD in a Dockerfile?",
            "What is a Docker network and what are the different network modes?",
            "What is a Docker registry and what is Docker Hub?",
        ],
        "experienced": [
            "How does Docker layer caching work and what Dockerfile instruction ordering maximises cache hits for a Python app?",
            "What is a multi-stage Docker build and how does it reduce the final image size?",
            "How would you secure a Docker container — what are the risks of running as root inside a container?",
            "What is the difference between bridge, host, and overlay networks in Docker?",
            "How does Docker's copy-on-write filesystem work with OverlayFS?",
            "How would you optimise a Docker image that is currently 2GB to be under 200MB?",
            "What are the trade-offs between Docker Compose and Kubernetes for orchestrating a multi-service app?",
            "How would you manage secrets in a Docker Swarm or Kubernetes deployment?",
            "How does Docker handle container resource limits — CPU and memory — and what happens when they are exceeded?",
            "What is a Docker health check and how does it integrate with container orchestrators like Kubernetes?",
        ],
    },

    # ── Kubernetes ────────────────────────────────────────────────────────────
    "kubernetes": {
        "fresher": [
            "What is Kubernetes and what problem does it solve?",
            "What is the difference between a Pod, Deployment, and Service in Kubernetes?",
            "What is a Kubernetes namespace and why would you use it?",
            "What is the difference between a ClusterIP, NodePort, and LoadBalancer service?",
            "What is a ConfigMap and a Secret in Kubernetes — how are they different?",
            "What is a ReplicaSet and how does it relate to a Deployment?",
            "What does kubectl get pods and kubectl describe pod do?",
            "What is a Kubernetes Ingress and when would you use it instead of a LoadBalancer?",
            "What is a liveness probe and a readiness probe in Kubernetes?",
            "What is a Persistent Volume and a Persistent Volume Claim?",
        ],
        "experienced": [
            "How does the Kubernetes scheduler decide which node to place a pod on?",
            "Explain Kubernetes resource requests and limits — what happens when a container exceeds its memory limit?",
            "How does Kubernetes horizontal pod autoscaling work and what metrics can trigger it?",
            "What is the difference between a StatefulSet and a Deployment — when must you use a StatefulSet?",
            "How does Kubernetes handle rolling updates and rollbacks — what is the maxSurge and maxUnavailable parameter?",
            "What is the Kubernetes control plane and what does each component do: API server, etcd, scheduler, controller manager?",
            "How would you implement zero-downtime deployments in Kubernetes?",
            "What are Kubernetes network policies and how would you use them to isolate namespaces?",
            "How does RBAC work in Kubernetes and how would you give a service account read-only access to pods?",
            "Explain how you would debug a pod that is stuck in CrashLoopBackOff.",
        ],
    },

    # ── AWS ───────────────────────────────────────────────────────────────────
    "aws": {
        "fresher": [
            "What is the difference between EC2, ECS, and Lambda in AWS?",
            "What is S3 and what types of data is it used to store?",
            "What is an IAM role and how is it different from an IAM user?",
            "What is the difference between a Security Group and a Network ACL in AWS?",
            "What is Amazon RDS and how does it differ from installing a database on an EC2 instance?",
            "What is a VPC and what are subnets in AWS?",
            "What is CloudWatch and what can you monitor with it?",
            "What is the difference between horizontal and vertical scaling in AWS?",
            "What is SQS and when would you use it instead of calling a service directly?",
            "What is an Elastic Load Balancer and what types exist in AWS?",
        ],
        "experienced": [
            "How would you design a highly available, fault-tolerant architecture on AWS for a web application?",
            "What is the difference between SQS standard queues and FIFO queues — when does ordering matter?",
            "How does AWS Lambda cold start work and what strategies reduce it for a latency-sensitive function?",
            "Explain the difference between S3 storage classes — when would you use Glacier vs Intelligent-Tiering?",
            "How does AWS auto scaling work with target tracking vs step scaling policies?",
            "What is the difference between an Application Load Balancer and a Network Load Balancer — when do you need each?",
            "How would you implement cross-region disaster recovery in AWS with RTO < 1 hour?",
            "What is AWS CloudFormation/CDK and how does infrastructure-as-code prevent configuration drift?",
            "How would you secure an S3 bucket that contains sensitive customer data — what AWS controls would you apply?",
            "Explain AWS VPC peering vs PrivateLink — when would you choose one over the other?",
        ],
    },

    # ── Machine Learning ──────────────────────────────────────────────────────
    "machine learning": {
        "fresher": [
            "What is the difference between supervised, unsupervised, and reinforcement learning?",
            "What is overfitting and how can you detect and prevent it?",
            "What is the difference between a training set, validation set, and test set?",
            "What is a confusion matrix and what metrics can you derive from it?",
            "What is the difference between classification and regression?",
            "What is gradient descent and what does the learning rate control?",
            "What is a neural network at a high level — what are layers, neurons, and activation functions?",
            "What is cross-validation and why is it more reliable than a single train/test split?",
            "What is feature engineering and why is it important?",
            "What is the bias-variance trade-off in machine learning?",
        ],
        "experienced": [
            "How does batch normalisation work and why does it help training deep networks?",
            "Explain the vanishing gradient problem — what causes it and how do residual connections address it?",
            "What is the difference between L1 and L2 regularisation — when would you prefer L1 for a model?",
            "How does the attention mechanism in transformers work — what problem does it solve over RNNs?",
            "How would you handle a severely class-imbalanced dataset for a fraud detection model?",
            "What is the difference between boosting and bagging — when does XGBoost outperform Random Forest?",
            "How would you deploy a machine learning model to production and monitor for data drift?",
            "What are the trade-offs between using a large pre-trained model vs training a smaller model from scratch?",
            "Explain how you would debug a model that performs well on the validation set but poorly in production.",
            "What is federated learning and in what scenarios would you use it over centralised training?",
        ],
    },

    # ── SQL (generic) ─────────────────────────────────────────────────────────
    "sql": {
        "fresher": [
            "What is the difference between DDL, DML, and DCL in SQL?",
            "What is a primary key and why should every table have one?",
            "What is the difference between WHERE and HAVING in a SQL query?",
            "How does GROUP BY work and what columns must appear in the SELECT clause when you use it?",
            "What is a JOIN — explain INNER JOIN vs LEFT JOIN with an example?",
            "What is a subquery and how is it different from a JOIN?",
            "What does DISTINCT do and when should you avoid it for performance?",
            "What is a view in SQL and what are its limitations?",
            "What is the difference between DELETE, TRUNCATE, and DROP?",
            "What is a stored procedure and how is it different from a function?",
        ],
        "experienced": [
            "How does a SQL query execute internally — what is the order of operations (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY)?",
            "What is a window function in SQL — write a query using ROW_NUMBER(), RANK(), and LAG()?",
            "How would you find and eliminate duplicate rows from a large table without downtime?",
            "What is an index seek vs index scan and what query patterns cause each one?",
            "How would you write a recursive CTE to traverse a hierarchical table?",
            "Explain the difference between optimistic and pessimistic locking in SQL databases.",
            "How would you optimise a query that JOINs three tables with millions of rows each?",
            "What is a covering index and how does it eliminate key lookups?",
            "How do database query planners work at a high level — what statistics do they use?",
            "What is normalisation — explain 1NF, 2NF, 3NF and give an example of denormalisation for performance?",
        ],
    },

    # ── Git ───────────────────────────────────────────────────────────────────
    "git": {
        "fresher": [
            "What is the difference between git merge and git rebase?",
            "What does git stash do and how do you apply stashed changes?",
            "What is the difference between git fetch and git pull?",
            "What is a git branch and why is branching cheap in git compared to other VCS?",
            "What does git reset --hard vs git reset --soft do?",
            "What is a merge conflict and how do you resolve one?",
            "What is a .gitignore file and what should you typically put in it?",
            "What is the difference between git add and git commit?",
            "What does git cherry-pick do?",
            "What is the difference between git clone and git fork?",
        ],
        "experienced": [
            "How does git's internal object model work — what are blobs, trees, commits, and tags?",
            "What is the difference between git merge --squash, --no-ff, and --ff-only and when would you use each?",
            "How would you recover a commit that was accidentally removed with git reset --hard?",
            "What is git bisect and how would you use it to find which commit introduced a bug?",
            "Explain what git reflog is and how it saved you from a mistake.",
            "What is a git hook and how would you use a pre-commit hook to enforce code quality?",
            "How does git rebase -i work and what are the risks of rebasing shared branches?",
            "What is the difference between git submodule and git subtree?",
            "How would you set up a GitFlow or trunk-based development workflow for a team of 10 engineers?",
            "What happens internally when you run git commit — what objects are created in the object store?",
        ],
    },

    # ── TypeScript ────────────────────────────────────────────────────────────
    "typescript": {
        "fresher": [
            "What is TypeScript and what advantages does it have over plain JavaScript?",
            "What is the difference between type and interface in TypeScript?",
            "What are generics in TypeScript and why are they useful?",
            "What is the difference between any, unknown, and never in TypeScript?",
            "What are TypeScript utility types — give examples of Partial, Required, and Pick?",
            "What is type narrowing in TypeScript and how do you use typeof and instanceof for it?",
            "What is the difference between optional chaining (?.) and non-null assertion (!) in TypeScript?",
            "What is an enum in TypeScript and what are its limitations?",
            "What is a union type vs an intersection type in TypeScript?",
            "How does TypeScript handle module resolution?",
        ],
        "experienced": [
            "What are conditional types in TypeScript — write a type that extracts the return type of a function?",
            "How does TypeScript's structural typing (duck typing) differ from nominal typing, and what are the trade-offs?",
            "What are mapped types in TypeScript and how would you use them to create a deep readonly type?",
            "Explain TypeScript's infer keyword with a practical example.",
            "How would you design a type-safe event emitter in TypeScript using generics?",
            "What are declaration merging and module augmentation in TypeScript — give a real use case?",
            "What are the performance implications of complex TypeScript type computations on compile time?",
            "How does TypeScript's control flow analysis work for type narrowing in complex conditionals?",
            "What is the difference between covariance and contravariance in TypeScript function types?",
            "How would you migrate a large JavaScript codebase to TypeScript incrementally without breaking production?",
        ],
    },

    # ── Redis ─────────────────────────────────────────────────────────────────
    "redis": {
        "fresher": [
            "What is Redis and what makes it different from a traditional database?",
            "What data structures does Redis support — give a use case for each?",
            "What is TTL in Redis and how do you set it on a key?",
            "What is the difference between Redis persistence modes: RDB and AOF?",
            "How would you use Redis as a cache in a web application?",
            "What is the difference between SET, GET, INCR, and EXPIRE commands in Redis?",
            "What is a Redis list and how does it differ from a set?",
            "What are Redis sorted sets and when would you use them?",
            "What is Redis pub/sub and what is a basic use case for it?",
            "What is the difference between a Redis cache miss and a cache hit?",
        ],
        "experienced": [
            "How does Redis handle single-threaded I/O and why is it still fast under high load?",
            "What is the difference between Redis Cluster and Redis Sentinel — when would you use each?",
            "How would you implement a distributed lock with Redis and what are the pitfalls of Redlock?",
            "How does Redis handle eviction when memory is full — what are the eviction policies and when would you use each?",
            "What are the consistency trade-offs between RDB snapshots and AOF logging in Redis?",
            "How would you implement a real-time leaderboard with Redis sorted sets for 1 million users?",
            "What is Redis Streams and how does it compare to Kafka for message queuing?",
            "How does Redis replication work and what happens to writes during a primary failure?",
            "Explain a cache stampede and how you would prevent it with Redis.",
            "How would you use Redis pipelines and Lua scripts to make multi-step operations atomic?",
        ],
    },

    # ── Spring Boot / Java ────────────────────────────────────────────────────
    "java": {
        "fresher": [
            "What is the difference between an interface and an abstract class in Java?",
            "What is the difference between == and .equals() in Java?",
            "What is the Java Collections Framework — what is the difference between ArrayList and LinkedList?",
            "What is the difference between checked and unchecked exceptions in Java?",
            "What are generics in Java and why are they useful?",
            "What is the difference between HashMap, LinkedHashMap, and TreeMap?",
            "What is the difference between StringBuilder and String in Java?",
            "What is multithreading in Java — what is the difference between Thread and Runnable?",
            "What are Java streams (java.util.stream) and how do they differ from I/O streams?",
            "What is garbage collection in Java and what does the JVM's GC do?",
        ],
        "experienced": [
            "How does the Java memory model work — what are the heap, stack, and metaspace?",
            "What is the difference between synchronized, volatile, and AtomicInteger for thread safety in Java?",
            "How does Java's ConcurrentHashMap achieve thread safety without a global lock?",
            "What are the different garbage collectors in Java (G1, ZGC, Shenandoah) and when would you choose each?",
            "Explain Java's CompletableFuture — how does it differ from Future and how do you compose async operations?",
            "How does Spring Boot's dependency injection work internally — what is a BeanFactory vs ApplicationContext?",
            "What is the difference between @Transactional on a class vs a method in Spring — what are the propagation modes?",
            "How would you diagnose a Java application with high CPU usage in production?",
            "What are virtual threads in Java 21 (Project Loom) and how do they change the concurrency model?",
            "How does JPA/Hibernate's first-level cache work and what is the N+1 select problem?",
        ],
    },

    # ── C++ ───────────────────────────────────────────────────────────────────
    "c++": {
        "fresher": [
            "What is the difference between a pointer and a reference in C++?",
            "What is RAII (Resource Acquisition Is Initialization) and why is it important in C++?",
            "What is the difference between stack and heap memory in C++?",
            "What are smart pointers in C++ — what is the difference between unique_ptr, shared_ptr, and weak_ptr?",
            "What is the difference between new/delete and malloc/free in C++?",
            "What is function overloading vs function overriding in C++?",
            "What is the difference between virtual and pure virtual functions?",
            "What is a copy constructor and when does C++ call it automatically?",
            "What is move semantics in C++11 and how does std::move work?",
            "What is a template in C++ and what is it used for?",
        ],
        "experienced": [
            "How does C++ template specialization and SFINAE work — give a practical example?",
            "What is the Rule of Five in modern C++ and when must you implement it?",
            "How does C++ virtual dispatch work internally — what is a vtable and how is it laid out in memory?",
            "What is undefined behaviour in C++ and how do tools like AddressSanitizer and Valgrind help detect it?",
            "How does std::atomic work in C++ and what are the memory ordering options?",
            "What is the difference between std::deque and std::vector in terms of memory layout and performance?",
            "How would you profile a C++ application to find cache misses and false sharing?",
            "What are C++20 concepts and how do they improve on SFINAE for template constraints?",
            "How does the C++ allocator model work and when would you write a custom allocator?",
            "What is coroutine support in C++20 and how does co_await differ from traditional async callbacks?",
        ],
    },

    # ── Data Science / Pandas / NumPy ─────────────────────────────────────────
    "pandas": {
        "fresher": [
            "What is the difference between a Pandas Series and a DataFrame?",
            "How do you handle missing values in a Pandas DataFrame?",
            "What is the difference between loc and iloc in Pandas?",
            "How do you merge two DataFrames in Pandas — what merge types are available?",
            "What is groupby in Pandas and how does it work with agg()?",
            "What is the difference between apply() and map() in Pandas?",
            "How do you filter rows in a DataFrame based on column values?",
            "What is the difference between copy() and a view in Pandas — why does it matter?",
            "How do you read a CSV file into a Pandas DataFrame and what common parameters does read_csv() take?",
            "What is pivot_table() in Pandas and how does it differ from groupby?",
        ],
        "experienced": [
            "How does Pandas store data internally — what are dtypes and why does object dtype have poor performance?",
            "How would you optimise a Pandas pipeline that processes a 10GB CSV file that doesn't fit in memory?",
            "What is vectorisation in Pandas/NumPy and why is it orders of magnitude faster than Python loops?",
            "What is the difference between using apply() and a vectorised NumPy operation — when should you avoid apply()?",
            "How does Pandas MultiIndex work and when would you use it over a flat index?",
            "What are Pandas extension types (Int64, StringDtype, ArrowDtype) and why were they introduced?",
            "How would you profile a slow Pandas pipeline to find the bottleneck?",
            "What is the difference between Pandas and Polars for data processing — when would you switch?",
            "How does NumPy broadcasting work — give an example where it would fail and how to fix it?",
            "What is Dask and how does it extend Pandas to handle out-of-core computation?",
        ],
    },

}

# ─────────────────────────────────────────────────────────────────────────────
# ALIAS MAP  — normalise tech stack input to question bank keys
# ─────────────────────────────────────────────────────────────────────────────

ALIASES = {
    # Python ecosystem
    "python":           "python",
    "python3":          "python",
    "py":               "python",
    "django":           "django",
    "fastapi":          "fastapi",
    "fast api":         "fastapi",
    "flask":            "flask",
    "pandas":           "pandas",
    "numpy":            "pandas",
    "data science":     "pandas",
    "scikit":           "machine learning",
    "sklearn":          "machine learning",
    "tensorflow":       "machine learning",
    "pytorch":          "machine learning",
    "keras":            "machine learning",
    "ml":               "machine learning",
    "machine learning": "machine learning",
    "ai":               "machine learning",
    "deep learning":    "machine learning",

    # JavaScript ecosystem
    "javascript":  "javascript",
    "js":          "javascript",
    "es6":         "javascript",
    "typescript":  "typescript",
    "ts":          "typescript",
    "react":       "react",
    "reactjs":     "react",
    "react.js":    "react",
    "next":        "react",
    "nextjs":      "react",
    "next.js":     "react",
    "node":        "nodejs",
    "nodejs":      "nodejs",
    "node.js":     "nodejs",
    "express":     "nodejs",
    "expressjs":   "nodejs",

    # Java / Spring
    "java":         "java",
    "spring":       "java",
    "spring boot":  "java",
    "springboot":   "java",
    "hibernate":    "java",
    "jvm":          "java",

    # C family
    "c++":     "c++",
    "cpp":     "c++",
    "c plus plus": "c++",

    # Databases
    "postgresql":  "postgresql",
    "postgres":    "postgresql",
    "psql":        "postgresql",
    "mysql":       "mysql",
    "mariadb":     "mysql",
    "mongodb":     "mongodb",
    "mongo":       "mongodb",
    "redis":       "redis",
    "sql":         "sql",
    "sqlite":      "sql",
    "oracle":      "sql",
    "mssql":       "sql",
    "sql server":  "sql",

    # DevOps / Cloud
    "docker":       "docker",
    "kubernetes":   "kubernetes",
    "k8s":          "kubernetes",
    "aws":          "aws",
    "amazon":       "aws",
    "ec2":          "aws",
    "lambda":       "aws",
    "s3":           "aws",
    "git":          "git",
    "github":       "git",
    "gitlab":       "git",
}


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def _parse_experience(experience_str: str) -> int:
    """Extract years of experience as an integer from a free-text string."""
    numbers = re.findall(r'\d+', str(experience_str))
    if numbers:
        return int(numbers[0])
    if "fresher" in experience_str.lower() or "entry" in experience_str.lower():
        return 0
    return 1  # default to fresher


def _resolve_tech(tech: str) -> str | None:
    """Map a raw tech name to a question bank key, or None if not found."""
    key = tech.strip().lower()
    return ALIASES.get(key) or (key if key in QUESTIONS else None)


def get_questions_for_stack(
    tech_stack_str: str,
    experience_str: str,
    questions_per_tech: int = 2,
) -> list[dict]:
    """
    Pick random, real interview questions from the bank for each technology
    in the candidate's stack, matched to their experience level.

    Args:
        tech_stack_str:     Raw comma-separated tech stack string from the candidate.
        experience_str:     Raw experience string (e.g. "3 years", "fresher", "5+").
        questions_per_tech: How many questions to pick per technology (default 2).

    Returns:
        List of dicts: [{"tech": "Python", "level": "experienced", "question": "..."}, ...]
    """
    years   = _parse_experience(experience_str)
    level   = "fresher" if years < 3 else "experienced"

    # Parse tech stack — split on commas, slashes, semicolons
    techs_raw = re.split(r'[,/;]+', tech_stack_str)
    techs_raw = [t.strip() for t in techs_raw if t.strip()]

    results   = []
    seen_keys = set()

    for tech_name in techs_raw:
        bank_key = _resolve_tech(tech_name)

        if not bank_key or bank_key in seen_keys:
            continue
        seen_keys.add(bank_key)

        pool = QUESTIONS[bank_key].get(level, [])
        if not pool:
            continue

        picked = random.sample(pool, min(questions_per_tech, len(pool)))

        for q in picked:
            results.append({
                "tech":     tech_name.title(),   # display name as-typed
                "level":    level,
                "question": q,
            })

    return results


def get_available_techs() -> list[str]:
    """Return a sorted list of all technology keys in the question bank."""
    return sorted(QUESTIONS.keys())


def get_question_count() -> dict:
    """Return total question counts per tech and level."""
    return {
        tech: {
            "fresher":    len(data.get("fresher", [])),
            "experienced": len(data.get("experienced", [])),
        }
        for tech, data in QUESTIONS.items()
    }