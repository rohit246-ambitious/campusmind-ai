# CampusMind API Contract

## Auth
POST /auth/register
POST /auth/login

## Categories
POST /categories (admin)
GET /categories

## Issues
POST /issues (multipart/form-data)
GET /issues (admin)
GET /issues/filter?category_id=
GET /issues/paginated?page=&limit=
PUT /issues/{id}/status

## Dashboard
GET /dashboard/stats (admin)

## Headers
Authorization: Bearer <JWT>
