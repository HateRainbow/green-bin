# Green Bin - AI-Powered Trash Classification System

A full-stack web application that uses AI to classify trash images and collect user feedback to improve classification accuracy.

## 🚀 Features

- **AI Image Classification**: Upload images and get instant trash classification using a fine-tuned transformer model
- **User Feedback System**: Submit corrections when AI misclassifies images
- **Analytics Dashboard**: View classification accuracy and feedback trends over time
- **Real-time Charts**: Visualize feedback data with interactive bar charts
- **RESTful API**: FastAPI backend with automatic documentation

## 🏗️ Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 18
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **ML Model**: Hugging Face Transformers (yangy50/garbage-classification)
- **Package Manager**: uv

### Frontend

- **Framework**: React 19 + TypeScript
- **Router**: TanStack Router v1 (file-based)
- **Build Tool**: Vite
- **UI Components**: shadcn/ui + Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios

## 📋 Prerequisites

- Python 3.11.6 or higher
- Node.js 20 or higher
- PostgreSQL 18 (or use Docker)
- Docker & Docker Compose (optional, for containerized setup)

## 🛠️ Installation & Setup

### Option 1: Local Development (Recommended for Development)

#### 1. Clone the Repository

```bash
git clone https://github.com/HateRainbow/green-bin.git
cd green-bin
```

#### 2. Set Up the Database

**Option A: Using Docker (Easiest)**

```bash
docker compose up db -d
```

#### 3. Set Up the Backend

```bash
cd backend

# Install uv (if not already installed)
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell):
# irm https://astral.sh/uv/install.ps1 | iex

# Create .env file
cp .env.example .env

# Edit .env and set your DATABASE_URL
# DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase

# Install dependencies
uv sync

# Download the AI model and train it on the datasets from kaggle
uv run python app/AI/train.py

# Run database migrations
uv run alembic upgrade head

# Start the backend server
uv run uvicorn app.app:app --reload --port 8080
```

The backend will be available at:

- API: http://localhost:8080
- API Docs: http://localhost:8080/docs

#### 4. Set Up the Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional - defaults work)
# Create .env.local if you need custom API URL
# VITE_API_URL=http://localhost:8080/api

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:3000

---

### Option 2: Docker (Recommended for Production)

This will start everything (database, backend, frontend) in containers.

```bash
# From the project root
docker compose up --build
```

**First time setup:**
The backend container will automatically:

1. Download the AI model (~200MB, takes a few minutes)
2. Set up the database
3. Run migrations
4. Start the server

**Access the application:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs

**View logs:**

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

**Stop services:**

```bash
docker compose down

# Stop and remove volumes (clears database)
docker compose down -v
```

---

## 📁 Project Structure

```
green-bin/
├── backend/
│   ├── app/
│   │   ├── AI/
│   │   │   ├── download_model.py    # Model download script
│   │   │   ├── pipeline.py          # AI inference pipeline
│   │   │   └── model/               # Model files (not committed)
│   │   ├── database/
│   │   │   └── core.py              # Database setup
│   │   ├── entities/
│   │   │   └── table.py             # SQLAlchemy models
│   │   ├── routes/
│   │   │   ├── picture.py           # Image upload & retrieval
│   │   │   ├── feedback.py          # Feedback submission
│   │   │   └── dashboard.py         # Analytics endpoint
│   │   ├── schemas/
│   │   │   └── feedback.py          # Pydantic schemas
│   │   ├── service/
│   │   │   ├── picture.py           # Picture business logic
│   │   │   └── feedback.py          # Feedback business logic
│   │   ├── alembic/                 # Database migrations
│   │   ├── app.py                   # FastAPI application
│   │   └── config.py                # Configuration
│   ├── dockerfile
│   ├── entrypoint.sh
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── __root.tsx           # Root layout + Context
│   │   │   ├── index.tsx            # Upload page
│   │   │   ├── $id.tsx              # Result & feedback page
│   │   │   └── dashboard.tsx        # Analytics dashboard
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   └── ui/                  # shadcn components
│   │   ├── api.ts                   # Axios configuration
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── DOCKER.md
└── README.md
```

---

## 🔧 Common Commands

### Backend

```bash
# Run the backend server
uv run uvicorn app.app:app --reload --port 8080

# Alternative (using app.py directly)
uv run app/app.py

# Download/update the AI model
uv run python app/AI/download_model.py

# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

### Frontend

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run serve

# Run tests
npm run test

# Add shadcn component
npx shadcn@latest add button

# Format code
npm run format
```

### Docker

```bash
# Build and start all services
docker compose up --build

# Start in detached mode
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f [service-name]

# Execute command in container
docker compose exec backend bash
docker compose exec frontend sh

# Rebuild specific service
docker compose up --build backend

# Remove all volumes (reset database)
docker compose down -v
```

---

## 🔄 Database Migrations

### Creating a New Migration

When you modify `backend/app/entities/table.py`:

```bash
cd backend

# Generate migration automatically
uv run alembic revision --autogenerate -m "Add new column"

# Review the generated migration in app/alembic/versions/

# Apply the migration
uv run alembic upgrade head
```

### Manual Migration

```bash
# Create empty migration
uv run alembic revision -m "custom migration"

# Edit the generated file in app/alembic/versions/
# Add your upgrade() and downgrade() logic

# Apply
uv run alembic upgrade head
```

---

## 🤖 AI Model

The project uses the [yangy50/garbage-classification](https://huggingface.co/yangy50/garbage-classification) model from Hugging Face.

**Model Details:**

- **Type**: Image Classification
- **Size**: ~200MB
- **Classes**: Various trash categories
- **Framework**: Transformers (PyTorch)

**Downloading the Model:**

The model is **NOT** committed to Git. You must download it:

**Local Development:**

```bash
cd backend
uv run python app/AI/download_model.py
```

**Docker:**
The model downloads automatically on first container start.

**Model Location:**

- Local: `backend/app/AI/model/`
- Docker: Inside the container at `/app/app/AI/model/`

---

## 🌐 API Endpoints

### Pictures

- `POST /api/picture` - Upload and classify an image

  - Body: FormData with `file` field
  - Returns: `{id, filename, label, confidence}`

- `GET /api/picture/{id}` - Get picture details
  - Returns: Picture data with base64-encoded image

### Feedback

- `POST /api/feedback/{id}` - Submit feedback for a classification
  - Body: `{is_correct: boolean, message?: string, correct_label?: string}`
  - Returns: Feedback record

### Dashboard

- `GET /api/dashboard` - Get analytics data
  - Returns: `{total_pictures, total_feedback, feedback_by_date[]}`

**Full API Documentation:**
Visit http://localhost:8080/docs when the backend is running.

---

## 🎨 Frontend Pages

### 1. Upload Page (`/`)

- Upload trash images
- File validation (images only)
- Automatic redirect to results

### 2. Result Page (`/:id`)

- Display uploaded image
- Show AI classification and confidence
- Submit feedback (correct/incorrect)
- Auto-fetch data on page refresh

### 3. Dashboard (`/dashboard`)

- Total pictures and feedback stats
- AI accuracy calculation
- Bar chart showing feedback trends over time
- Daily breakdown of correct vs incorrect classifications

---

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError:**

```bash
# Make sure you're in the backend directory
cd backend
uv sync
```

**Database Connection Error:**

```bash
# Check if PostgreSQL is running
# If using Docker:
docker compose up db -d

# Verify .env file has correct DATABASE_URL
cat .env
```

**Model Not Found:**

```bash
# Download the model
uv run python app/AI/download_model.py
```

**Migration Issues:**

```bash
# Check current migration version
uv run alembic current

# Reset database (WARNING: deletes all data)
uv run alembic downgrade base
uv run alembic upgrade head
```

### Frontend Issues

**Port Already in Use:**

```bash
# Change port in package.json or run:
npm run dev -- --port 3001
```

**API Connection Refused:**

- Ensure backend is running on port 8080
- Check `VITE_API_URL` in `.env.local`
- Verify CORS settings in `backend/app/app.py`

**Build Errors:**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Port Conflicts:**
Edit `docker-compose.yml` to change port mappings:

```yaml
ports:
  - "3001:3000" # Change first number (host port)
```

**Container Won't Start:**

```bash
# Check logs
docker compose logs backend

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up
```

**Database Connection Failed:**

```bash
# Wait for database health check
docker compose up db
# Wait for "database system is ready to accept connections"
# Then start other services
docker compose up backend frontend
```

---

## 🧪 Testing

### Backend

```bash
cd backend
# Add pytest if not installed
uv add pytest pytest-asyncio httpx

# Run tests
uv run pytest
```

### Frontend

```bash
cd frontend
npm run test
```

---

## 📝 Environment Variables

### Backend (.env)

```env
# Required
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
```

### Frontend (.env.local)

```env
# Optional - defaults to http://localhost:8080/api
VITE_API_URL=http://localhost:8080/api
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set strong database credentials
- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Configure logging and monitoring
- [ ] Set up backup for database
- [ ] Use a reverse proxy (nginx/Caddy)
- [ ] Set up CI/CD pipeline
- [ ] Configure proper error handling
- [ ] Enable rate limiting

### Deployment Options

1. **Docker Compose** (on VPS)
2. **Kubernetes** (for scaling)
3. **Cloud Services** (AWS ECS, Google Cloud Run)
4. **Platform as a Service** (Heroku, Railway, Render)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **HateRainbow** - [GitHub](https://github.com/HateRainbow)

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the transformer models
- [yangy50](https://huggingface.co/yangy50) for the garbage-classification model
- [shadcn/ui](https://ui.shadcn.com/) for the beautiful UI components
- [TanStack](https://tanstack.com/) for the amazing router
