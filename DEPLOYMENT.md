# Cloud Deployment Guide

This guide provides instructions for deploying the Personality Prediction application to various cloud providers.

## Render Deployment (Recommended)

Render offers a simple deployment process with free tiers for both web services and static sites.

### Step 1: Deploy the Backend API

1. Log in to [Render](https://render.com)
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: `personality-prediction-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn server:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`
   - Plan: Free
5. Click "Create Web Service"
6. Wait for deployment to complete
7. Note the URL of your deployed API (e.g., `https://personality-prediction-api.onrender.com`)

### Step 2: Clean up and prepare frontend locally

Before trying to deploy the frontend on Render, clean up the node_modules directory:

```bash
# Remove node_modules folder
rm -rf frontend/node_modules

# Make sure the package.json has a proper build script
# Then commit and push without node_modules
git add .gitignore
git commit -m "Add gitignore to exclude node_modules"
git add frontend/
git commit -m "Add frontend without node_modules"
git push
```

### Step 3: Deploy the Frontend

1. From Render dashboard, click "New" and select "Static Site"
2. Connect to the same GitHub repository
3. Configure:
   - Name: `personality-prediction-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`
4. Add environment variable:
   - Key: `REACT_APP_API_URL`
   - Value: The URL of your backend API from Step 1
5. Click "Create Static Site"

## Heroku Deployment

Heroku offers one of the simplest deployment options for containerized applications.

### Setup

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to your Heroku account:
   ```
   heroku login
   ```

### Deployment Steps

1. Create a new Heroku application:
   ```
   heroku create personality-prediction-app
   ```

2. Set the stack to container:
   ```
   heroku stack:set container
   ```

3. Push your code to Heroku:
   ```
   git push heroku main
   ```

4. Open the deployed application:
   ```
   heroku open
   ```

### Database Considerations

For production use, consider using Heroku Postgres instead of SQLite:

1. Add the Postgres add-on:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

2. Update your application to use the Postgres database URL from the environment variables.

## AWS Elastic Beanstalk Deployment

AWS Elastic Beanstalk provides an easy way to deploy containerized applications.

### Setup

1. Install the [AWS CLI](https://aws.amazon.com/cli/) and [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
2. Configure your AWS credentials:
   ```
   aws configure
   ```

### Deployment Steps

1. Initialize your EB CLI repository:
   ```
   eb init -p docker personality-prediction
   ```

2. Create an environment and deploy:
   ```
   eb create personality-prediction-env
   ```

3. Open the deployed application:
   ```
   eb open
   ```

### Database Considerations

For production, consider using Amazon RDS instead of SQLite:

1. Create an RDS instance in the AWS console
2. Update your application to use the RDS connection details

## Google Cloud Run Deployment

Google Cloud Run is ideal for containerized web applications with automatic scaling.

### Setup

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Login to your Google Cloud account:
   ```
   gcloud auth login
   ```
3. Set your project:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

### Deployment Steps

1. Build and push your container to Google Container Registry:
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/personality-prediction
   ```

2. Deploy to Cloud Run:
   ```
   gcloud run deploy personality-prediction --image gcr.io/YOUR_PROJECT_ID/personality-prediction --platform managed --allow-unauthenticated
   ```

### Database Considerations

For production, consider using Google Cloud SQL:

1. Create a Cloud SQL instance in the Google Cloud console
2. Update your application to use the Cloud SQL connection details

## Microsoft Azure App Service Deployment

Azure App Service provides a managed hosting environment for containerized applications.

### Setup

1. Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Login to your Azure account:
   ```
   az login
   ```

### Deployment Steps

1. Create a resource group:
   ```
   az group create --name personality-prediction-group --location eastus
   ```

2. Create an Azure Container Registry (ACR):
   ```
   az acr create --name personalitypredictionacr --resource-group personality-prediction-group --sku Basic --admin-enabled true
   ```

3. Build and push your container to ACR:
   ```
   az acr build --registry personalitypredictionacr --image personality-prediction:latest .
   ```

4. Create an App Service plan:
   ```
   az appservice plan create --name personality-prediction-plan --resource-group personality-prediction-group --is-linux --sku B1
   ```

5. Create a web app:
   ```
   az webapp create --name personality-prediction-app --resource-group personality-prediction-group --plan personality-prediction-plan --deployment-container-image-name personalitypredictionacr.azurecr.io/personality-prediction:latest
   ```

### Database Considerations

For production, consider using Azure Database for PostgreSQL:

1. Create an Azure Database for PostgreSQL in the Azure portal
2. Update your application to use the PostgreSQL connection details

## Production Considerations

Regardless of your cloud provider, consider these production best practices:

1. **Environment Variables**: Store sensitive information in environment variables or secret management services
2. **Persistent Storage**: Use cloud database services rather than SQLite for production workloads
3. **Logging**: Implement proper logging for troubleshooting in production
4. **Monitoring**: Set up monitoring tools to track application performance and usage
5. **CI/CD**: Configure continuous integration and deployment pipelines
6. **Scaling**: Understand the scaling capabilities and limitations of your chosen provider
7. **Costs**: Monitor usage to prevent unexpected billing surprises

## Troubleshooting

If you encounter issues during deployment:

1. Check the logs provided by your cloud provider
2. Verify that all environment variables are correctly set
3. Ensure your container runs properly in your local environment before deploying
4. Review the cloud provider's documentation for specific error messages
