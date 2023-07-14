echo "Deploying Frontend..."
cd frontend2
export REACT_APP_API_URL=/api
export REACT_APP_API_KEY=qPzT2B7AhloXs9BEgmQcoaBuMpabQO6s
npm run build
aws s3 sync build/ s3://mateomonedas-frontend