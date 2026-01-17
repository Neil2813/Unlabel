# Unlabel
*The Only Food Intelligence System with Transparent Autonomous AI Agents*

## 🎯 One-Line Value Proposition

**"The only food intelligence system that combines autonomous AI agents with transparent, explainable decisions - helping consumers understand ingredients without the cognitive overload."**

---

## 🤖 What Makes Unlabel Revolutionary?

### **Autonomous Multi-Agent Architecture** (Not Just Another AI App)

Unlabel is **AI-native first** - not an app with AI added on. We use specialized autonomous agents working in coordination, each with a focused role:

1. **🎯 Intent Classifier Agent** - Understands your real question (quick yes/no, comparison, risk check, curiosity)
2. **🔬 Ingredient Interpreter Agent** - Converts ingredients into structured, neutral signals
3. **⚖️ Decision Engine Agent** - Rule-based, transparent scoring system
4. **💬 Explanation Agent** - Translates decisions into consumer-friendly language
5. **📚 Ingredient Translator Agent** - Explains complex scientific terms simply

**Why This Matters:**
- ✅ **Transparency**: See exactly which agent made which decision
- ✅ **Reliability**: If one agent fails, others continue functioning
- ✅ **Explainability**: Each step is traceable and auditable
- ✅ **Scalability**: Agents can be improved and scaled independently

**Competitors**: Single black-box AI model → unexplainable decisions  
**Unlabel**: Specialized autonomous agents → transparent, explainable, reliable

---

## 🔑 Top 5 Unique Selling Points

### 1. **Transparent Rule-Based Decisions** (Not Black Box AI)
- **What**: Decisions use explicit, auditable rules you can inspect
- **Why**: Trust, consistency, regulatory compliance, user education
- **Example**: *"Rated Occasional because: minimally processed (+3), strong fiber/protein support (+2), added sugars present (-1.5) = score 3.5"*

### 2. **Progressive Disclosure UI** (Minimal Cognitive Load)
- **What**: Quick insight + verdict first, details on demand
- **Why**: Fast decisions, no information overload, mobile-friendly
- **Impact**: **2-second decisions** for quick users, full depth for researchers

### 3. **Ingredient Translation Layer** (Democratizes Knowledge)
- **What**: Auto-translates complex scientific terms into simple explanations
- **Why**: No chemistry degree needed, reduces fear, empowers decisions
- **Example**: *"Sodium Benzoate" → "A preservative that prevents mold and bacteria growth"*

### 4. **Neutral Signal Extraction** (No Agenda)
- **What**: Extracts facts, not opinions; users decide what matters
- **Why**: No hidden biases, user autonomy, regulatory safety
- **Impact**: Pure information without pushing any diet philosophy

### 5. **Honest Uncertainty Communication**
- **What**: Explicitly flags when information is incomplete or ambiguous
- **Why**: Honesty builds trust and safety
- **Example**: Shows confidence notes, ambiguity flags, and uncertainty reasons

---

## 🚀 The Problem We Solve

### **The Consumer Health Information Gap**

Food labels are optimized for regulatory compliance, not human understanding. Long ingredient lists, unfamiliar chemical names, and conflicting health guidance leave consumers uncertain.

**What Existing Solutions Get Wrong:**
- ❌ Surface raw data instead of insight
- ❌ Use black-box AI with unexplainable decisions
- ❌ Create information overload
- ❌ Require high-friction manual input
- ❌ Have hidden agendas or diet-specific biases

**What Unlabel Does Differently:**
- ✅ Transparent autonomous agents with explainable decisions
- ✅ Progressive disclosure - see only what you need
- ✅ Intent-aware processing - answers YOUR question
- ✅ Ingredient translation - complex terms explained simply
- ✅ Neutral analysis - we inform, you decide

## 🏗️ Architecture Overview

This project is built as a modern full-stack application connecting a fluid React frontend with a powerful Python/FastAPI backend powered by Google's Gemini 2.5 Flash model and integrated with Open Food Facts API.

### 📂 Project Structure
```
Unlabel/
├── Frontend/          # React + TypeScript + Tailwind CSS
├── Backend/           # FastAPI + SQLAlchemy + Gemini AI
└── README.md          # This file
```

---

## 🎨 Frontend Architecture (`/Frontend`)

### Technology Stack
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS with custom Glassmorphism design system
- **Routing:** React Router DOM v6
- **State Management:** React Context API
- **HTTP Client:** Axios
- **UI Components:** Radix UI primitives + custom components
- **Icons:** Lucide React

### Directory Structure
```
Frontend/src/
├── components/
│   ├── layout/
│   │   └── Header.tsx              # Global navigation header
│   ├── sections/
│   │   └── HowItWorksOrbital.tsx   # Landing page sections
│   └── ui/
│       ├── AIInput.tsx             # AI chat input component
│       ├── FoodScanner.tsx         # Camera/image upload
│       ├── GlassCard.tsx           # Glassmorphic card component
│       ├── FloatingSeeds.tsx       # Animated background
│       └── [60+ Radix UI components]
├── contexts/
│   └── AuthContext.tsx             # Authentication state management
├── hooks/
│   └── [Custom React hooks]
├── lib/
│   ├── api.ts                      # Axios instance with interceptors
│   └── utils.ts                    # Utility functions
├── pages/
│   ├── Home.tsx                    # Landing page
│   ├── Copilot.tsx                 # AI chat interface for analysis
│   ├── FoodSearch.tsx              # Global food product search
│   ├── History.tsx                 # User analysis history
│   ├── Login.tsx                   # Authentication
│   ├── Register.tsx                # User registration
│   ├── Profile.tsx                 # User profile management
│   └── NotFound.tsx                # 404 page
├── App.tsx                         # Root component with routing
├── main.tsx                        # Application entry point
└── index.css                       # Global styles + design tokens
```

### Key Features
1. **Design System**
   - Custom Glassmorphism aesthetic with watermelon-inspired color palette
   - Dark theme with deep greens (primary) and soft reds (secondary)
   - Reusable glass card components with glow effects
   - Smooth animations and transitions

2. **Pages & Routes**
   - `/` - Landing page with hero and features
   - `/analyze` - AI-powered food label analysis (chat interface)
   - `/analyze/:id` - View specific analysis from history
   - `/food-search` - Search global food products database
   - `/history` - User's past analyses
   - `/login` & `/register` - Authentication
   - `/profile` - User profile management

3. **State Management**
   - AuthContext for global authentication state
   - JWT token storage and automatic request injection
   - Protected routes with authentication checks

4. **API Integration**
   - Centralized Axios instance (`lib/api.ts`)
   - Automatic JWT token attachment
   - Request/response interceptors
   - Error handling

---

## ⚙️ Backend Architecture (`/Backend`)

### Technology Stack
- **Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **AI Model:** Google Gemini 2.5 Flash (`google-generativeai`)
- **Authentication:** JWT tokens with Argon2 password hashing
- **External APIs:** Open Food Facts API
- **Validation:** Pydantic models

### Directory Structure
```
Backend/app/
├── ai/
│   ├── models.py                   # AnalysisHistory SQLAlchemy model
│   ├── schemas.py                  # Pydantic request/response schemas
│   ├── service.py                  # FoodReasoningEngine (Gemini integration)
│   └── router.py                   # AI analysis endpoints
├── auth/
│   ├── models.py                   # User SQLAlchemy model
│   ├── schemas.py                  # Auth request/response schemas
│   ├── dependencies.py             # JWT verification & user extraction
│   ├── utils.py                    # Password hashing utilities
│   └── router.py                   # Auth endpoints (login, register)
├── food/
│   └── router.py                   # Open Food Facts API integration
├── profile/
│   ├── schemas.py                  # Profile update schemas
│   └── router.py                   # User profile endpoints
├── db/
│   ├── base.py                     # SQLAlchemy Base class
│   ├── database.py                 # Database connection & session
│   └── init_db.py                  # Database initialization
├── config/
│   └── [Configuration files]
└── main.py                         # FastAPI application entry point
```

### API Endpoints

#### AI Analysis (`/api/analyze`)
- `POST /autonomous/text` - Autonomous agent text analysis (multi-step workflow)
- `POST /autonomous/image` - Autonomous agent image analysis (multimodal)
- `POST /decision` - Transparent Decision Engine (with consumer explanation)
- `POST /decision/image` - Decision Engine for image input
- `POST /compare` - Compare two products side-by-side

### Core Components

#### 1. **FoodReasoningEngine** (`ai/service.py`)
The heart of the AI system:
- Constructs persona-based system prompts
- Handles multimodal input (text + images)
- Enforces strict JSON schema for reliable parsing
- Implements uncertainty handling
- Returns structured analysis with:
  - Insight summary
  - Detailed reasoning
  - Trade-offs (pros/cons)
  - Uncertainty notes

#### 2. **Authentication System** (`auth/`)
- Argon2 password hashing for security
- JWT token generation and validation
- Protected route decorators
- User session management

#### 3. **Database Models**
- **User**: Authentication and profile data
- **AnalysisHistory**: Stores all AI analyses with full results
- Relationships: User ↔ AnalysisHistory (one-to-many)

#### 4. **Open Food Facts Integration** (`food/router.py`)
- Case-insensitive product search
- Partial name matching
- Comprehensive product data extraction:
  - Nutrition grades (Nutri-Score, Eco-Score)
  - Nutritional values
  - Ingredients and allergens
  - Manufacturing details
  - Product images

### Data Flow
```
User Input → Frontend → API Request → Backend Router
                                          ↓
                                    Authentication Check
                                          ↓
                                    Service Layer (AI/Database)
                                          ↓
                                    External APIs (Gemini/Open Food Facts)
                                          ↓
                                    Response Processing
                                          ↓
                                    JSON Response → Frontend → UI Update
```

### Security Features
- JWT-based authentication
- Argon2 password hashing
- Protected API endpoints
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)

### Database Schema
```sql
users
├── id (Primary Key)
├── email (Unique)
├── name
├── hashed_password
└── created_at

analysis_history
├── id (Primary Key)
├── user_id (Foreign Key → users.id)
├── input_type (text/image)
├── input_content
├── full_result (JSON)
├── title
└── created_at
```

---

## 🤖 Autonomous Agent System

### **The Transparent Decision Pipeline**

Unlike competitors who use a single "black box" AI, Unlabel employs a **multi-agent system** where each agent has a specific, auditable role:

```
User Input → Agent Coordination Pipeline → Transparent Output
```

### **Agent Coordination Flow**

```mermaid
User Input (Text/Image)
       ↓
┌──────────────────────────────────────┐
│  🎯 Intent Classifier Agent          │
│  "What is the user really asking?"   │
│  Output: intent_type, confidence     │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  🔬 Ingredient Interpreter Agent     │
│  "What are the neutral facts?"       │
│  Output: structured signals          │
│  - processing_level: minimal/moderate│
│  - sugar_dominant: true/false        │
│  - fiber_protein_support: strong/weak│
│  - key_nutrients: [...]              │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  ⚖️ Decision Engine Agent            │
│  "Apply transparent rules"           │
│  Rule-based scoring (deterministic)  │
│  Output: verdict, score, reasoning   │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  📚 Ingredient Translator Agent      │
│  "Explain complex terms simply"      │
│  Output: ingredient_cards            │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  💬 Explanation Agent                │
│  "Translate to human language"       │
│  Output: quick_insight, why_it_matters│
└──────────────────────────────────────┘
       ↓
Structured Response → Frontend → Progressive Disclosure UI
```

### **Why Multi-Agent Architecture?**

#### **1. Transparency**
Each agent's decision is recorded and can be audited:
```json
{
  "intent_classification": {
    "agent": "IntentClassifier",
    "intent": "quick_yes_no",
    "confidence": 0.92
  },
  "ingredient_analysis": {
    "agent": "IngredientInterpreter",
    "signals": {
      "processing_level": "minimal",
      "sugar_dominant": false
    }
  },
  "decision": {
    "agent": "DecisionEngine",
    "verdict": "Daily",
    "score": 4.5,
    "reasoning": "minimally_processed(+3), strong_fiber_protein(+2), no_added_sugars(+0.5)"
  }
}
```

#### **2. Reliability**
- **Fallback Mechanisms**: If one agent fails, others continue
- **Error Isolation**: Agent errors don't cascade
- **Graceful Degradation**: Can provide partial results

#### **3. Explainability**
- **Audit Trail**: See exactly which agent contributed what
- **Rule Transparency**: Decision Engine uses explicit rules, not learned weights
- **Confidence Tracking**: Each agent reports confidence levels

#### **4. Scalability**
- **Independent Scaling**: Scale agents based on their specific load
- **Parallel Processing**: Multiple agents can work simultaneously
- **Easy Updates**: Improve one agent without affecting others

### **Agent Implementation Details**

#### **Intent Classifier Agent**
```python
# Classifies user intent before processing
Intent Types:
  - quick_yes_no: "Is this healthy?"
  - comparison: "Which is better?"
  - risk_check: "Is this safe for me?"
  - curiosity: "Tell me about this product"

Output: { intent_type, confidence, focus_areas[] }
```

#### **Ingredient Interpreter Agent**
```python
# Extracts neutral, structured signals
Signals Extracted:
  - processing_level: minimal/moderate/ultra
  - sugar_dominant: boolean
  - fiber_protein_support: none/weak/moderate/strong
  - key_nutrients: array
  - allergens: array
  - additives: array

Output: { signals, confidence_notes, ambiguity_flags[] }
```

#### **Decision Engine Agent**
```python
# Rule-based, deterministic scoring
Scoring Rules (Transparent):
  minimally_processed → +3 points
  strong_fiber_protein → +2 points
  moderate_fiber_protein → +1 point
  added_sugars_present → -1.5 points
  sugar_dominant → -2 points
  ultra_processed → -3 points

Verdict Thresholds:
  Daily: score >= 4
  Occasional: score >= 1
  Limit: score < 1

Output: { verdict, score, key_signals[], reasoning }
```

#### **Ingredient Translator Agent**
```python
# Translates complex terms to simple language
Input: "Sodium Benzoate, Xanthan Gum, Ascorbic Acid"

Output: {
  "Sodium Benzoate": {
    "simple_name": "Preservative",
    "function": "Prevents mold and bacteria growth",
    "safety": "Generally recognized as safe (GRAS)"
  },
  "Xanthan Gum": {
    "simple_name": "Emulsifier",
    "function": "Helps ingredients blend smoothly",
    "derived_from": "Fermented sugars"
  },
  "Ascorbic Acid": {
    "simple_name": "Vitamin C",
    "function": "Antioxidant and preservative",
    "benefit": "Essential nutrient"
  }
}
```

#### **Explanation Agent**
```python
# Generates consumer-friendly explanations
Input: Structured decision data
Output: {
  "quick_insight": "One sentence (max 15 words)",
  "why_it_matters": "Actionable context (2-3 bullets, max 12 words each)",
  "when_it_makes_sense": "Usage context",
  "what_to_know": "Important caveats"
}

Style Guidelines:
  - Concise (max word limits enforced)
  - Simple (no jargon)
  - Actionable ("Pair with protein" not "Consider macronutrient balance")
  - Calm (no fear-mongering)
```

### **Competitive Comparison**

| Feature | Unlabel (Multi-Agent) | Competitors (Single AI) |
|---------|-----------------------|-------------------------|
| **Decision Transparency** | ✅ Each agent's contribution visible | ❌ Black box output |
| **Auditability** | ✅ Full audit trail | ❌ Cannot explain decisions |
| **Error Handling** | ✅ Graceful degradation | ❌ Complete failure |
| **Scalability** | ✅ Independent agent scaling | ⚠️ Monolithic scaling |
| **Maintainability** | ✅ Update agents independently | ❌ Retrain entire model |
| **Cost Efficiency** | ✅ Rules for decisions (no LLM cost) | ❌ LLM for all processing |
| **Consistency** | ✅ Deterministic decisions | ❌ Variable outputs |
| **Explainability** | ✅ Traceable reasoning | ❌ "AI says so" |

---


## ⚡ Workflow
1.  **Conversational Input:** User chats with the AI or shows a label in a fluid message stream.
2.  **Inference:** The AI Reasoning Engine (Backend) processes the visual/textual data.
3.  **Analysis:** Ingredients are identified, and nutritional context is extracted.
4.  **Reasoning:** The model evaluates trade-offs (pros/cons), health implications, and uncertainties.
5.  **Output:** Structured insights are presented as interactive cards within the chat.
6.  **History:** All conversations and analyses are stored for the user to review later.

## 🛠️ Setup & Running

### Prerequisites
*   Node.js & npm
*   Python 3.10+
*   Google Gemini API Key

### Quick Start
1.  **Backend:**
    ```bash
    cd Backend
    pip install -r requirements.txt
    # Set GEMINI_API_KEY in .env
    uvicorn app.main:app --reload
    ```
2.  **Frontend:**
    ```bash
    cd Frontend
    npm install
    npm run dev
    ```

## 📡 Real-Time Streaming Implementation

### **Server-Sent Events (SSE) Architecture**

Unlabel uses **Server-Sent Events (SSE)** for real-time progressive updates during analysis. Instead of waiting for a complete response, users see each step as it completes.

#### **Streaming Flow:**
```
User Query
    ↓
Frontend EventSource Connection
    ↓
Backend SSE Stream (/api/analyze/autonomous/text/stream)
    ↓
Progressive Events:
  1. step_start: "Analyzing ingredients..."
  2. step_complete: Initial analysis results
  3. step_start: "Running decision engine..."
  4. step_complete: Decision engine results
  5. step_start: "Creating summary..."
  6. step_complete: Synthesis results
  7. complete: Final comprehensive result
```

#### **User Experience:**
- **Before (POST):** 6-8 second blank loading screen
- **After (Streaming):** Real-time updates every 2-3 seconds
- **Impact:** Feels 2-3x faster despite same total time

#### **Implementation Details:**

**Backend Endpoint:** `Backend/app/ai/router.py`
```python
@router.get("/autonomous/text/stream")
async def autonomous_analyze_text_stream(text: str, user_query: str = None):
    """Streams analysis results as Server-Sent Events"""
    async def event_generator():
        # Step 1: Initial Analysis
        yield f"data: {json.dumps({'event': 'step_start', ...})}\\n\\n"
        result = await ai_service.analyze_text(text)
        yield f"data: {json.dumps({'event': 'step_complete', ...})}\\n\\n"
        
        # Step 2: Decision Engine
        yield f"data: {json.dumps({'event': 'step_start', ...})}\\n\\n"
        decision = await coordinator.process(request)
        yield f"data: {json.dumps({'event': 'step_complete', ...})}\\n\\n"
        
        # Final result
        yield f"data: {json.dumps({'event': 'complete', 'result': {...}})}\\n\\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Frontend Client:** `Frontend/src/pages/Copilot.tsx`
```typescript
const eventSource = new EventSource(streamUrl);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch (data.event) {
    case 'step_start':
      setLoadingProgress({ message: data.message });
      break;
    case 'step_complete':
      // Store partial results
      break;
    case 'complete':
      // Display final result
      eventSource.close();
      break;
  }
};
```

### **Production Configuration**

#### **Environment Variables:**

**Frontend (.env.production):**
```bash
VITE_API_URL=https://unlabel.onrender.com/api
```

**Backend (.env):**
```bash
ENV=production
FRONTEND_URL=https://unlabel-eight.vercel.app
GEMINI_API_KEY1=your-api-key
GEMINI_API_KEY2=backup-key  # Optional failover
```

#### **Deployment Platforms:**
- **Frontend:** Vercel (automatic HTTPS, zero-config SSE support)
- **Backend:** Render (HTTP/2 enabled, persistent connections)

#### **CORS Configuration:**
Backend automatically allows streaming from configured frontend URLs:
```python
# Backend/app/main.py
ALLOWED_ORIGINS = [
    FRONTEND_URL,  # Production
    "http://localhost:5173",  # Development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Deployment Checklist:**

**Vercel (Frontend):**
1. Set environment variable: `VITE_API_URL=https://unlabel.onrender.com/api`
2. Build command: `npm run build`
3. Deploy (automatic on push)

**Render (Backend):**
1. Set environment variables:
   - `ENV=production`
   - `FRONTEND_URL=https://unlabel-eight.vercel.app`
   - `GEMINI_API_KEY1=your-key`
2. Deploy (automatic on push)

**Testing Streaming:**
```bash
# Test backend endpoint directly
curl -N "https://unlabel.onrender.com/api/analyze/autonomous/text/stream?text=coca%20cola"

# Expected output:
# data: {"event": "step_start", "step": 1, ...}
# data: {"event": "step_complete", "step": 1, ...}
# data: {"event": "complete", "result": {...}}
```

#### **Documentation:**
- **Full Streaming Guide:** `STREAMING_COMPLETE.md`
- **Production Setup:** `STREAMING_PRODUCTION_CONFIG.md`
- **Deployment Checklist:** `DEPLOYMENT_CHECKLIST.md`


## 🎯 Key Capabilities & Differentiators

### **Autonomous Agent Features**
*   **🤖 Multi-Agent Coordination:** Five specialized agents working transparently together
*   **🔍 Intent-Aware Processing:** Classifies what you're really asking before analyzing
*   **⚖️ Rule-Based Transparency:** See exactly how decisions are scored (+3, -1.5, etc.)
*   **📊 Structured Signal Extraction:** Converts ingredients to neutral, auditable facts
*   **🎓 Automatic Ingredient Translation:** Complex scientific terms explained simply

### **User Experience Features**
*   **⚡ 2-Second Decisions:** Quick insight + verdict for fast choices
*   **📖 Progressive Disclosure:** Details only when you want them - no information overload
*   **🎨 Visual Clarity:** Color-coded verdict badges (Daily/Occasional/Limit)
*   **💬 Conversational Interface:** Chat naturally with the AI copilot
*   **🔄 Intent Adaptation:** Response style matches your question type

### **Technical Features**
*   **📸 Multimodal Analysis:** Understands both text and images
*   **🌐 Partial Data Resilience:** Can read partially obscured or blurry labels
*   **✅ Honest Uncertainty:** Explicitly flags when information is incomplete
*   **📚 History Tracking:** Saves past analyses for longitudinal insights
*   **🌍 Global Food Database:** Search and explore 3+ million products from Open Food Facts

### **Trust & Safety Features**
*   **🎯 No Hidden Agenda:** Neutral analysis without diet-specific biases
*   **⚖️ Regulatory Compliant:** Avoids medical claims, provides information not advice
*   **🔒 Audit Trail:** Every agent decision is traceable and explainable
*   **📏 Consistent Results:** Deterministic decision engine (same input = same output)
*   **💯 User Autonomy:** We inform, you decide what matters to you

