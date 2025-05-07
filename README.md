# Gretchen North Artshop

**Live Site:** [https://gretchen-north-art.onrender.com](https://gretchen-north-art.onrender.com)  
**Repository:** [github.com/DaniNorth/gretchen-north-art](https://github.com/DaniNorth/gretchen-north-art)  
**Trello Board:** [Gretchen Artshop Project](https://trello.com/b/SbiztkQb/gretchen-artshop-project)

![Screenshot of Homepage](./A_screenshot_of_the_homepage_of_Gretchen_North_Art.png)

## About the Project

**Gretchen North Artshop** is an online eCommerce platform built with Django for showcasing and selling original artworks by Gretchen North. Visitors can browse unique art pieces, add items to their wishlist or cart, and check out securely. The goal is to provide an intuitive, elegant, and mobile-responsive experience for both casual viewers and serious collectors.

The site also includes an admin portal with support for AI-enhanced listing tools (in progress) and image-based detection to streamline catalog management.

---

## MVP Features

- Tailwind CSS styled frontend with coehsive styling throughout
- Dynamic gallery of available artworks with filters and sorting
- Wishlist feature with drag-and-drop to cart
- Shopping cart system with hold-timer logic
- Cloudinary integration for secure image uploads
- Customer profile page with editable info and wishlist management
- Django admin for internal management
- Full CRUD for wishlist items (secure per user)
- Secure login/logout/signup using Django AllAuth
- Deployed to Render with Whitenoise + Tailwind static bundling
- Sqaure deployed in sandbox mode

---

##  Stretch Goals & Next Steps

- Square checkout integration for live sales
- Admin-facing AI listing assistant for auto-tagging, sizing, and pricing
- Mailchimp newsletter integration
- Customer order history + receipt system
- Blog/news section with artist updates
- Artwork categorization and search filtering
- SEO optimization and analytics tracking
- Barcode or QR generator for art labels
- Auto-calculated shipping via EasyPost (in progress)
- Advanced inventory dashboard for admin

---

## Technologies Used

- **Django 5.2** (backend & templating)
- **PostgreSQL** (database on Render)
- **Tailwind CSS v4.1.5** (responsive styling)
- **Cloudinary** (image hosting)
- **Django AllAuth** (authentication)
- **JavaScript** (dynamic behavior, drag-and-drop, timers)
- **Trello** (project planning)
- **Render.com** (deployment)
- **ChatGPT** (used for brainstorming and code polishing)
- **Canva Pro** (branding and design assets)
- **GitHub** (version control)

---

## Getting Started

Clone the repo:

```bash
git clone https://github.com/DaniNorth/gretchen-north-art.git
cd gretchen-north-art
Create your .env file and add required variables:

env
Copy
Edit
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_ENV=development
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
SQUARE_ACCESS_TOKEN=optional
SQUARE_LOCATION_ID=optional
Install dependencies and run the dev server:

bash
Copy
Edit
pip install -r requirements.txt
npm install
npm run dev
python manage.py runserver
  Attribution
Tailwind CSS: tailwindcss.com

Cloudinary: cloudinary.com

Render: render.com

AllAuth: django-allauth.readthedocs.io

Code snippets generated or debugged using ChatGPT 4

Developer Notes
This project is part of a General Assembly final Django capstone. Some advanced features (AI automation, Square integration) are in-progress and not deployed in the MVP. AI-enhanced tasks are currently disabled or under local testing and finetuning and are expected to be running by June 15, 2025.

