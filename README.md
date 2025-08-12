# NepFlix - Movie Ticket Booking System

A comprehensive Django-based movie ticket booking platform with advanced features including reviews, analytics, cancellation/refund system, and mobile-first responsive design.

## 🎬 Features

### Core Functionality
- **Movie Management**: Complete CRUD operations for movies with posters, trailers, and metadata
- **Theater Management**: Multi-theater support with location and capacity management
- **Seat Booking**: Interactive seat selection with real-time availability
- **Payment Processing**: Multiple payment method support (Stripe, Razorpay, Cash)
- **User Authentication**: Secure registration, login, and profile management

### 🎯 New Features Implemented

#### 1. Movie Review & Rating System
- **User Reviews**: Authenticated users can write detailed reviews with ratings (1-5 stars)
- **Review Management**: Users can edit or delete their own reviews
- **Rating Analytics**: Average ratings, review counts, and rating distribution
- **Review Guidelines**: Built-in guidelines for constructive reviews
- **Review Validation**: Minimum character requirements and content validation

#### 2. Admin Dashboard with Analytics
- **Comprehensive Analytics**: Revenue tracking, booking trends, user statistics
- **Interactive Charts**: Daily revenue trends, payment method distribution
- **Real-time Metrics**: 
  - Total revenue, bookings, users, movies
  - Monthly/weekly revenue tracking
  - Top movies by bookings and ratings
  - Genre popularity statistics
- **User Analytics**: Registration trends, active users, top customers
- **Booking Analytics**: Performance metrics by movie and theater

#### 3. Movie Booking Cancellation & Refund System
- **Flexible Cancellation Policy**:
  - 24+ hours before showtime: 100% refund
  - 2-24 hours before showtime: 50% refund
  - Less than 2 hours: No refund
- **Cancellation Workflow**: 
  - Reason selection and additional notes
  - Confirmation checkboxes
  - Automatic seat release
  - Payment status updates
- **Refund Processing**: Automatic refund calculation and processing
- **Cancellation History**: Complete audit trail of cancellations

#### 4. Dark Mode Toggle
- **Theme Persistence**: Remembers user's theme preference
- **Smooth Transitions**: CSS transitions for theme switching
- **Comprehensive Styling**: All components support both light and dark themes
- **Accessibility**: High contrast ratios and readable text in both modes
- **CSS Variables**: Centralized color management for easy customization

#### 5. Mobile-First Responsive Design
- **Bootstrap 5**: Latest responsive framework
- **Mobile Optimization**: Touch-friendly interfaces and optimized layouts
- **Progressive Enhancement**: Works on all device sizes
- **Performance**: Optimized images and lazy loading
- **Accessibility**: ARIA labels and keyboard navigation

## 🛠 Technology Stack

- **Backend**: Django 4.2.23
- **Database**: SQLite (production-ready for PostgreSQL)
- **Frontend**: Bootstrap 5, jQuery, Chart.js
- **Styling**: CSS3 with CSS Variables for theming
- **Icons**: Font Awesome 6
- **Charts**: Chart.js for analytics visualization

## 📁 Project Structure

```
NepFlix/
├── accounts/          # User authentication and profiles
├── movies/           # Movie management and reviews
├── booking/          # Booking system and cancellations
├── theaters/         # Theater management
├── analytics/        # Admin dashboard and analytics
├── templates/        # HTML templates
│   ├── accounts/
│   ├── movies/
│   ├── booking/
│   └── analytics/
├── static/          # CSS, JS, images
└── media/           # User uploads (posters, etc.)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NepFlix
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Analytics: http://localhost:8000/analytics/dashboard/

## 📊 Key Features in Detail

### Movie Review System
```python
# Models
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Analytics Dashboard
```python
# Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Revenue statistics
    total_revenue = Payment.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Booking trends
    recent_bookings = Booking.objects.filter(
        booking_date__gte=last_7_days
    ).count()
```

### Cancellation System
```python
# Models
class Booking(models.Model):
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    @property
    def can_cancel(self):
        return (show_datetime - current_time) > timedelta(hours=24)
```

### Dark Mode Implementation
```css
:root {
    --primary-color: #e50914;
    --text-color: #333;
    --bg-color: #fff;
    --card-bg: #f8f9fa;
}

[data-bs-theme="dark"] {
    --text-color: #f8f9fa;
    --bg-color: #1a1a1a;
    --card-bg: #2d2d2d;
}
```

## 🎨 UI/UX Features

### Responsive Design
- **Mobile-first approach**: Optimized for mobile devices
- **Flexible grid system**: Bootstrap 5 responsive grid
- **Touch-friendly**: Large buttons and touch targets
- **Fast loading**: Optimized images and lazy loading

### Dark Mode
- **Theme toggle**: Moon/sun icon in navigation
- **Persistent preference**: Stored in localStorage
- **Smooth transitions**: CSS transitions for theme switching
- **Comprehensive coverage**: All components themed

### Interactive Elements
- **Star ratings**: Interactive star rating system
- **Seat selection**: Visual seat map with availability
- **Filter system**: Real-time movie filtering
- **Search functionality**: Advanced search with multiple criteria

## 📈 Analytics Features

### Revenue Tracking
- Daily, weekly, monthly revenue trends
- Payment method distribution
- Revenue by movie and theater
- Refund tracking and analysis

### User Analytics
- Registration trends
- Active user tracking
- User behavior analysis
- Top customers by spending

### Booking Analytics
- Booking trends over time
- Movie performance metrics
- Theater performance comparison
- Cancellation rate analysis

## 🔧 Configuration

### Environment Variables
```python
# settings.py
SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# Payment settings
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_key'
STRIPE_SECRET_KEY = 'sk_test_your_key'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Endpoints

### Movies
- `GET /movies/` - List all movies
- `GET /movies/<id>/` - Movie details
- `POST /movies/<id>/review/` - Add review
- `DELETE /movies/review/<id>/delete/` - Delete review

### Bookings
- `GET /booking/my-bookings/` - User bookings
- `GET /booking/booking/<id>/` - Booking details
- `POST /booking/booking/<id>/cancel/` - Cancel booking

### Analytics (Admin only)
- `GET /analytics/dashboard/` - Admin dashboard
- `GET /analytics/booking/` - Booking analytics
- `GET /analytics/users/` - User analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: support@nepflix.com
- Documentation: [Link to docs]
- Issues: [GitHub Issues]

## 🔮 Future Enhancements

- [ ] Real-time seat availability updates
- [ ] Push notifications for booking confirmations
- [ ] Advanced search with filters
- [ ] Social media integration
- [ ] Loyalty program
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics with machine learning

---

**NepFlix** - Your premier destination for movie ticket booking! 🎬✨ 