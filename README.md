# Tally Subscriber Manager

A web application that captures form submissions from Tally, stores subscriber data in a database, and allows sending newsletters to subscribers.

## Features

- Receive webhook data from Tally forms
- Store subscriber information in MongoDB
- Send newsletters to subscribers using Gmail SMTP
- Modern React frontend with Next.js
- Docker-based backend for easy deployment on Render

## Project Structure

```
tally-subscriber-manager/
├── backend/             # Flask API backend
│   ├── app/             # Application code
│   ├── app.py           # Main entry point
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend
│   ├── src/             # Source code
│   ├── public/          # Static assets
│   └── package.json     # Node.js dependencies
├── docker/              # Docker configuration
│   └── Dockerfile       # Backend Dockerfile
└── docker-compose.yml   # Local development setup
```

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (for frontend development)
- A Tally account with a form
- Gmail account with App Password

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Backend
MONGO_URI=mongodb://mongo:27017/tally_subscribers
SECRET_KEY=your_secret_key
GMAIL_ADDRESS=your_gmail_address@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
TALLY_WEBHOOK_SECRET=your_tally_webhook_secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Running Locally

1. Start the backend and MongoDB:

```bash
docker-compose up -d
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Start the frontend development server:

```bash
npm run dev
```

4. Access the application at http://localhost:3000

### Setting up Tally Webhook

1. Go to your Tally form dashboard
2. Click on the form you want to connect
3. Go to "Integrations" in the sidebar
4. Select "Webhooks"
5. Click "Connect"
6. Enter your webhook URL: `https://your-domain.com/api/webhook/tally`
7. Optional: Add a signing secret for enhanced security
8. Click "Save" to activate the webhook

## Deployment

### Backend Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Select "Docker" as the environment
4. Set the required environment variables
5. Deploy the service

### Frontend Deployment on Vercel

1. Connect your GitHub repository to Vercel
2. Configure the build settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/.next`
3. Set the environment variables
4. Deploy the application

## License

MIT
