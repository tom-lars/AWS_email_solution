# Serverless Bulk Email Sending via API Gateway, SQS, Lambda, and SES

This project allows sending emails through a public API securely and scalably without losing emails even when SES throttles.

---

## Architecture

- **API Gateway**: Accepts `POST` requests with email details.
- **Lambda 1 (Submit Function)**: Receives API requests and puts the message in an **SQS queue**.
- **SQS Queue**: Buffers email send requests.
- **Lambda 2 (Send Function)**: Listens to SQS, reads messages, and sends emails via **Amazon SES**.
- **Dead Letter Queue (DLQ)**: Stores messages that fail processing.

---

## Deployment Steps

### 1. Setup Amazon SES
- Verify your sender email address (or domain).
- Move SES out of sandbox if required.

### 2. Create SQS Queues
- Main Queue (e.g., `EmailQueue`)
- Dead Letter Queue (e.g., `EmailDLQ`)
- Attach DLQ to the main queue (e.g., after 5 receive failures).

### 3. Create Lambda Functions

- **Lambda 1 (SubmitToSQS):**
  - Trigger: API Gateway (HTTP POST)
  - Action: Push message to SQS

- **Lambda 2 (SendEmailFromSQS):**
  - Trigger: SQS (event source)
  - Action: Read message and send email using SES

### 4. Setup API Gateway
- Create a REST API.
- Create a `POST /send-email` endpoint.
- Integrate the endpoint with Lambda 1 (Submit function).

### 5. IAM Roles
- Create IAM roles for both Lambda functions with appropriate permissions (see below).

---

## API Request Format

Send a POST request to API Gateway with this body:

```json
{
  "subject": "Your Subject Here",
  "body": "This is the body of the email.",
  "recipients": [
    "user1@example.com",
    "user2@example.com"
  ]
}
