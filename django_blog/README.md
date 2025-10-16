# Django Blog Application

A comprehensive blog application built with Django featuring user authentication, blog post management, and comment functionality.

## Features

### User Authentication
- User registration with email validation
- Login/logout functionality
- User profile management with bio and profile pictures
- Secure password handling with Django's built-in hashing

### Blog Post Management (CRUD)
- **Create**: Authenticated users can create new blog posts
- **Read**: All users can view blog posts and post details
- **Update**: Post authors can edit their own posts
- **Delete**: Post authors can delete their own posts
- Search functionality across posts

### Comment System
- Add comments to blog posts (authenticated users only)
- Edit and delete own comments
- Comment validation (10-1000 characters)
- Real-time character count

### Security Features
- CSRF protection on all forms
- LoginRequiredMixin for protected views
- UserPassesTestMixin for authorization
- Input validation and sanitization

## Project Structure
