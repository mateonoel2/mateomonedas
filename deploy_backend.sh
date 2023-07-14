echo "Deploying Backend..."
cd backend2
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 641580831416.dkr.ecr.us-east-2.amazonaws.com
docker build -t mateomonedas-backend .
docker tag mateomonedas-backend:latest 641580831416.dkr.ecr.us-east-2.amazonaws.com/mateomonedas-backend:latest
docker push 641580831416.dkr.ecr.us-east-2.amazonaws.com/mateomonedas-backend:latest
cd aws_deploy
eb deploy