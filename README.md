# Serverless URL Shortener

A small serverless application built on AWS that shortens long URLs and redirects visitors from the short link back to the original.

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
[API Gateway] --> [Lambda: create_short_url.py] --> [DynamoDB: UrlShortener table]
   |
   v  (GET /{shortCode})
[API Gateway] --> [Lambda: redirect_url.py] --> [DynamoDB: UrlShortener table] --> 302 redirect
```
## Progress

- ✅ DynamoDB table (`URLShortener`) created in AWS (eu-west-1... wait, eu-west-1 Ireland)
- ✅ `create-short-url` and `redirect-url` Lambda functions deployed and tested
- ✅ API Gateway wired up with POST /create and GET /{shortCode}, CORS enabled
- ✅ Front-end hosted on S3, live and fully working end-to-end
- ✅ Full pipeline tested: create a short URL → redirect works correctly

**Why this design:**
- **S3** hosts the front-end as a static site — no server to manage, cheap and simple for a form-only UI.
- **API Gateway** exposes two HTTP endpoints: one to create short URLs, one to handle redirects.
- **Lambda** runs the logic for both endpoints — pay only when it's invoked, no idle server cost.
- **DynamoDB** stores the shortCode -> longUrl mapping as a key-value pair, which is exactly the access pattern DynamoDB is built for (fast lookups by primary key).

## DynamoDB Table Setup

- Table name: `UrlShortener`
- Partition key: `shortCode` (String)

## Deployment Steps

1. **Create the DynamoDB table** (`UrlShortener`, partition key `shortCode`).
2. **Create two Lambda functions**:
   - `create_short_url` using `create_short_url.py`
   - `redirect_url` using `redirect_url.py`
   - Attach an IAM role to both with `dynamodb:GetItem` and `dynamodb:PutItem` permissions on the table.
3. **Set up API Gateway**:
   - `POST /create` -> triggers `create_short_url` Lambda
   - `GET /{shortCode}` -> triggers `redirect_url` Lambda
   - Enable CORS on the `/create` route.
4. **Update the `BASE_URL`** environment variable in `create_short_url.py`'s Lambda config to your deployed API Gateway invoke URL.
5. **Update `API_ENDPOINT`** in `index.html` to match your `/create` route.
6. **Deploy `index.html` to an S3 bucket** with static website hosting enabled.

