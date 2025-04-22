pip install pipenv
pipenv install --deploy --ignore-pipfile

cd theme
npm install
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css
cd ..

python manage.py collectstatic --no-input
python manage.py migrate
