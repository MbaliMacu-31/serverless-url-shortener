# Serverless URL Shortener

A small serverless application built on AWS that shortens long URLs and redirects visitors from the short link back to the original.

**Live site:** http://mbali-url-shortener-2026.s3-website-eu-west-1.amazonaws.com

## Demo Video
[Link to your 5-10 min unlisted YouTube demo here]

## Architecture

```
User (browser)
   |
   v
[S3 Static Website] --- index.html (the form)
   |
   v  (POST /create)
[API Gateway] --> [Lambda: create_short_url.py] --> [DynamoDB: URLShortener table]
   |
   v  (GET /{shortCode})
[API Gateway] --> [Lambda: redirect_url.py] --> [DynamoDB: URLShortener table] --> 302 redirect
```

## Progress

- ✅ DynamoDB table (`URLShortener`) created in AWS, region eu-west-1 (Ireland)
- ✅ `create-short-url` and `redirect-url` Lambda functions deployed and tested
- ✅ API Gateway wired up with POST /create and GET /{shortCode}, CORS enabled
- ✅ Front-end hosted on S3: redesigned with custom typography/colors, copy-to-clipboard button, a "recently shortened" session list, and an architecture section explaining the live AWS pipeline
- ✅ Full pipeline tested end-to-end: create a short URL → redirect works correctly

**Why this design:**
- **S3** hosts the front-end as a static site — no server to manage, cheap and simple for a form-only UI.
- **API Gateway** exposes two HTTP endpoints: one to create short URLs, one to handle redirects.
- **Lambda** runs the logic for both endpoints — pay only when it's invoked, no idle server cost.
- **DynamoDB** stores the shortCode -> longUrl mapping as a key-value pair, which is exactly the access pattern DynamoDB is built for (fast lookups by primary key).

## DynamoDB Table Setup

- Table name: `URLShortener`
- Partition key: `shortCode` (String)

## Deployment Steps

1. **Create the DynamoDB table** (`URLShortener`, partition key `shortCode`).
2. **Create two Lambda functions**:
   - `create_short_url` using `create_short_url.py`
   - `redirect_url` using `redirect_url.py`
   - Attach an IAM role to both with `dynamodb:GetItem` and `dynamodb:PutItem` permissions on the table.
   - Set the `TABLE_NAME` environment variable to `URLShortener` on both functions.
   - Set the `BASE_URL` environment variable on `create-short-url` to your deployed API Gateway invoke URL.
3. **Set up API Gateway**:
   - `POST /create` -> triggers `create_short_url` Lambda
   - `GET /{shortCode}` -> triggers `redirect_url` Lambda
   - Enable CORS on the `/create` route (allow methods POST, OPTIONS; origin `*`).
   - Deploy to a `prod` stage.
4. **Update `API_ENDPOINT`** in `index.html` to your deployed API Gateway invoke URL, ending in `/create`.
5. **Deploy `index.html` to an S3 bucket** with static website hosting enabled and a public-read bucket policy.

## What I'd add with more time
- Custom short codes (let users pick their own)
- Click analytics (count how many times a short URL was visited)
- Expiry dates for short URLs
- Rate limiting to prevent abuse

## What I learned
- How API Gateway routes HTTP requests to specific Lambda functions, and why CORS needs explicit configuration for a browser-based front-end calling a different domain
- DynamoDB's key-value access pattern and why it fits this use case
- Debugging a case-sensitive table name mismatch between an environment variable and the actual DynamoDB table
- IAM least-privilege permissions for Lambda-to-DynamoDB access