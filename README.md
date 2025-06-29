# Supply Genie - Create Supply Chain

A comprehensive AI-powered supply chain management system that helps businesses discover, evaluate, and connect with reliable suppliers. Built with FastAPI, LangChain, and MongoDB.

## 🚀 Features

- **Intelligent Supplier Discovery**: Uses AI agents to search and evaluate suppliers from multiple sources
- **MongoDB Integration**: Stores and queries existing supplier data efficiently
- **Web Research**: Leverages Tavily API for real-time supplier information gathering
- **Smart Filtering**: Advanced search capabilities with location, price, certification filters
- **RESTful API**: Clean, documented API endpoints for easy integration
- **CORS Support**: Ready for frontend integration with cross-origin support

## 🛠️ Tech Stack

- **Backend**: FastAPI with Python 3.12
- **AI/ML**: LangChain, LangGraph, OpenAI GPT models
- **Database**: MongoDB with text search indexing
- **Search**: Tavily API for web research and data extraction
- **Logging**: Loguru for structured logging
- **Deployment**: Docker support with Cloud Run optimization

## 📋 Prerequisites

- Python 3.12+
- MongoDB database
- OpenAI API key
- Tavily API key (free credits available at https://tavily.com)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd supply-genie-create-supply-chain
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. Install Dependencies

**Option A: Using pip**

```bash
pip install -r requirements.txt
```

**Option B: Using uv (recommended)**

```bash
uv sync
```

### 4. Configure Environment Variables

Edit `.env` file with your credentials:

```env
# OpenAI API key for ChatOpenAI
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Tavily API key (get free credits at https://tavily.com)
TAVILY_API_KEY=tvly-dev-your-tavily-key-here

# MongoDB connection URI
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Override OpenAI model (optional)
MODEL_NAME=gpt-4o-mini
```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

### Production Mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

### Using Docker

```bash
# Build the image
docker build -t supply-genie .

# Run the container
docker run -p 8080:8080 --env-file .env supply-genie
```

The API will be available at `http://localhost:8080`

## 📖 API Documentation

### Base URL

```
http://localhost:8080
```

### Interactive Documentation

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

---

## 🛠️ API Endpoints

### 1. Health Check

**GET** `/`

Simple health check endpoint to verify the service is running.

#### Response

```json
{
  "message": "Hello World"
}
```

#### Example

```bash
curl -X GET "http://localhost:8080/"
```

---

### 2. Get Supply Chain Recommendations

**POST** `/api/v1/supply-chain/recommendations`

The main endpoint for discovering suppliers based on your requirements. Uses AI agents to search existing databases and perform web research to find the best suppliers.

#### Request Body

```json
{
  "query": "string (required, 1-2000 characters)",
  "chat_history": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ] // optional
}
```

#### Parameters

| Parameter      | Type   | Required | Description                                                  |
| -------------- | ------ | -------- | ------------------------------------------------------------ |
| `query`        | string | Yes      | Detailed description of supplier requirements (1-2000 chars) |
| `chat_history` | array  | No       | Previous conversation context for follow-up queries          |

#### Response

```json
{
  "suppliers": [
    {
      "company_name": "string",
      "location": "string",
      "rating": 0.0,
      "price_range": "string (in USD format: '$X-Y USD')",
      "lead_time": "string",
      "moq": "string",
      "certifications": ["string"],
      "specialties": ["string"],
      "response_time": "string (quantified: 'X-Y hours/days')",
      "contact": "string"
    }
  ]
}
```

#### Response Fields

| Field            | Type   | Description                       | Example                            |
| ---------------- | ------ | --------------------------------- | ---------------------------------- |
| `company_name`   | string | Official company name             | "ABC Manufacturing Ltd"            |
| `location`       | string | Company location/headquarters     | "Shanghai, China"                  |
| `rating`         | float  | Company rating (0-5 scale)        | 4.5                                |
| `price_range`    | string | Price range in USD                | "$50-100 USD"                      |
| `lead_time`      | string | Manufacturing/delivery lead time  | "2-3 weeks"                        |
| `moq`            | string | Minimum order quantity            | "1000 units"                       |
| `certifications` | array  | Quality/compliance certifications | ["ISO 9001", "FDA"]                |
| `specialties`    | array  | Company specializations           | ["Electronics", "Medical Devices"] |
| `response_time`  | string | Response time for inquiries       | "2-4 hours"                        |
| `contact`        | string | Contact information               | "contact@company.com"              |

---

## 📝 Examples

### Example 1: Basic Electronics Supplier Search

**Request:**

```bash
curl -X POST "http://localhost:8080/api/v1/supply-chain/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need suppliers for electronic components, specifically microcontrollers and sensors. Looking for reliable manufacturers in Asia with competitive pricing, ISO certifications, and fast response times."
  }'
```

**Response:**

```json
{
  "suppliers": [
    {
      "company_name": "TechFlow Electronics",
      "location": "Shenzhen, China",
      "rating": 4.7,
      "price_range": "$5-25 USD",
      "lead_time": "2-3 weeks",
      "moq": "1000 units",
      "certifications": ["ISO 9001", "RoHS", "CE"],
      "specialties": ["Microcontrollers", "Sensors", "IoT Components"],
      "response_time": "2-4 hours",
      "contact": "sales@techflow-electronics.com"
    },
    {
      "company_name": "AsiaChip Manufacturing",
      "location": "Taipei, Taiwan",
      "rating": 4.5,
      "price_range": "$8-30 USD",
      "lead_time": "1-2 weeks",
      "moq": "500 units",
      "certifications": ["ISO 9001", "ISO 14001", "OHSAS 18001"],
      "specialties": ["Semiconductors", "Custom ICs", "Sensors"],
      "response_time": "1-2 days",
      "contact": "inquiry@asiachip.com.tw"
    }
  ]
}
```

### Example 2: Textile Supplier Search with Chat History

**Request:**

```bash
curl -X POST "http://localhost:8080/api/v1/supply-chain/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Actually, I need organic cotton suppliers specifically for t-shirt manufacturing",
    "chat_history": [
      {
        "role": "user",
        "content": "I need textile suppliers for clothing manufacturing"
      },
      {
        "role": "assistant",
        "content": "I can help you find textile suppliers. What specific type of textiles and clothing items are you looking to manufacture?"
      }
    ]
  }'
```

**Response:**

```json
{
  "suppliers": [
    {
      "company_name": "Green Cotton Co.",
      "location": "Gujarat, India",
      "rating": 4.8,
      "price_range": "$3-8 USD",
      "lead_time": "3-4 weeks",
      "moq": "5000 yards",
      "certifications": ["GOTS", "OCS", "OEKO-TEX"],
      "specialties": [
        "Organic Cotton",
        "Sustainable Textiles",
        "T-shirt Fabric"
      ],
      "response_time": "4-6 hours",
      "contact": "orders@greencotton.in"
    },
    {
      "company_name": "EcoTextile Solutions",
      "location": "Istanbul, Turkey",
      "rating": 4.6,
      "price_range": "$4-10 USD",
      "lead_time": "2-3 weeks",
      "moq": "3000 yards",
      "certifications": ["GOTS", "Cradle to Cradle", "BCI"],
      "specialties": [
        "Organic Fabrics",
        "Eco-friendly Dyeing",
        "Apparel Textiles"
      ],
      "response_time": "3-5 hours",
      "contact": "sales@ecotextile.com.tr"
    }
  ]
}
```

### Example 3: Packaging Materials Search

**Request:**

```bash
curl -X POST "http://localhost:8080/api/v1/supply-chain/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Looking for sustainable packaging suppliers for food products. Need biodegradable containers, boxes, and wrapping materials. Prefer suppliers in North America with FDA approval and competitive bulk pricing."
  }'
```

**Response:**

```json
{
  "suppliers": [
    {
      "company_name": "EcoPackage America",
      "location": "Portland, Oregon, USA",
      "rating": 4.9,
      "price_range": "$15-45 USD",
      "lead_time": "1-2 weeks",
      "moq": "2000 units",
      "certifications": ["FDA", "USDA Organic", "BPI Certified"],
      "specialties": [
        "Biodegradable Containers",
        "Food-Safe Packaging",
        "Compostable Materials"
      ],
      "response_time": "1-2 hours",
      "contact": "info@ecopackageamerica.com"
    },
    {
      "company_name": "Green Box Solutions",
      "location": "Toronto, Ontario, Canada",
      "rating": 4.4,
      "price_range": "$12-40 USD",
      "lead_time": "2-3 weeks",
      "moq": "1500 units",
      "certifications": ["Health Canada", "FSC", "SFI"],
      "specialties": [
        "Corrugated Boxes",
        "Sustainable Packaging",
        "Custom Food Containers"
      ],
      "response_time": "2-3 hours",
      "contact": "sales@greenboxsolutions.ca"
    }
  ]
}
```

---

## 🔍 How It Works

The system uses an intelligent agent-based approach:

1. **Requirements Analysis**: AI analyzes your query to understand specific needs
2. **Database Search**: Queries existing supplier database using MongoDB text search
3. **Web Research**: Uses Tavily API to find new suppliers from web sources
4. **Data Extraction**: Extracts detailed supplier information from company websites
5. **Evaluation**: AI evaluates and ranks suppliers based on your criteria
6. **Response**: Returns top suppliers with complete, verified information

## 🗄️ Database Schema

### Suppliers Collection

```javascript
{
  "_id": ObjectId,
  "company_name": String,
  "location": String,
  "rating": Number,
  "price_range": String,
  "lead_time": String,
  "moq": String,
  "certifications": [String],
  "specialties": [String],
  "response_time": String,
  "contact": String,
  "created_at": Date,
  "updated_at": Date
}
```

## 🔒 Error Handling

### Common Error Responses

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid input)
- `422`: Validation Error
- `500`: Internal Server Error

### Example Error Response

```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_main.py::test_health_check
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build
docker build -t supply-genie .

# Run
docker run -p 8080:8080 --env-file .env supply-genie
```

### Docker Compose (Optional)

```yaml
version: "3.8"
services:
  supply-genie:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - MONGO_URI=${MONGO_URI}
      - MODEL_NAME=${MODEL_NAME}
```

## 🌐 Cloud Deployment

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/supply-genie

# Deploy to Cloud Run
gcloud run deploy supply-genie \
  --image gcr.io/PROJECT_ID/supply-genie \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

## 📊 Monitoring and Logging

The application uses structured logging with Loguru. Logs include:

- Request/response tracking
- Agent execution steps
- Database operations
- Error handling

### Log Levels

- `INFO`: General operation info
- `DEBUG`: Detailed debugging info
- `WARNING`: Non-critical issues
- `ERROR`: Error conditions

## 🔧 Configuration

### Environment Variables

| Variable         | Required | Default       | Description                   |
| ---------------- | -------- | ------------- | ----------------------------- |
| `OPENAI_API_KEY` | Yes      | -             | OpenAI API key for LLM        |
| `TAVILY_API_KEY` | Yes      | -             | Tavily API key for web search |
| `MONGO_URI`      | Yes      | -             | MongoDB connection string     |
| `MODEL_NAME`     | No       | `gpt-4o-mini` | OpenAI model to use           |

### Advanced Configuration

Edit `src/config.py` for advanced settings:

```python
# Agent configuration
AGENT_MAX_SUPPLIERS = 10
AGENT_RECURSION_LIMIT = 50
DEFAULT_REMAINING_STEPS = 10

# Query limits
MAX_QUERY_LENGTH = 2000
MAX_EXTRACT_URLS = 10

# LLM settings
LLM_TEMPERATURE = 0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:

1. Check the [API documentation](http://localhost:8080/docs)
2. Review the logs for error details
3. Ensure all environment variables are set correctly
4. Verify MongoDB connection and API keys

## 📈 Roadmap

- [ ] Add supplier comparison features
- [ ] Implement caching for improved performance
- [ ] Add supplier verification workflows
- [ ] Create supplier rating system
- [ ] Add export functionality (CSV, PDF)
- [ ] Implement real-time notifications
- [ ] Add multi-language support

---

**Built with ❤️ using FastAPI, LangChain, and MongoDB**
