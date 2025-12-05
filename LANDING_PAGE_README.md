# Landing Page Documentation

## Overview
A stunning, professional landing page has been created for your Laptop Price Prediction website. The page features a modern dark theme with vibrant animations and glassmorphic design elements.

## Features

### 🎨 Design Elements
- **Animated Background**: Floating gradient orbs with smooth blob animations
- **Glassmorphic Cards**: Frosted glass effect with backdrop blur
- **Grid Overlay**: Subtle grid pattern for depth
- **Gradient Accents**: Indigo, purple, and pink color scheme

### 🎯 Interactive Components
- **Live Calculator**: Real-time price estimation with smooth animations
- **Brand Selection**: Visual radio buttons for Apple, Dell, Razer, and Asus
- **RAM Slider**: Custom-styled range slider with visual feedback
- **Storage & Condition Dropdowns**: Sleek select menus
- **GPU Toggle**: Smooth toggle switch for discrete GPU option
- **Animated Price Display**: Price updates with smooth easing animation

### 📱 Responsive Design
- Mobile-first approach
- Adapts to all screen sizes
- Touch-friendly controls

### ✨ Animations
- Blob animations on background orbs
- Hover effects on all interactive elements
- Smooth transitions throughout
- Price counter animation
- Micro-interactions on buttons and links

## File Structure
```
backend/
├── templates/
│   ├── landing.html    # New landing page
│   └── index.html      # Original app
└── app.py              # Updated with /landing route
```

## Routes
- **`/`** - Professional landing page (default homepage)
- **`/app`** - Main laptop price predictor application

## How to Access
1. Make sure Flask is running:
   ```bash
   cd backend
   python app.py
   ```

2. Open in browser:
   - **Landing Page (Default)**: http://127.0.0.1:5000/
   - **Main App**: http://127.0.0.1:5000/app

When you run the Flask application, it will automatically display the landing page!

## Technologies Used
- **Tailwind CSS**: Utility-first CSS framework (via CDN)
- **Lucide Icons**: Beautiful icon library
- **Inter Font**: Modern, professional typography
- **Vanilla JavaScript**: Smooth animations and interactions

## Customization

### Colors
The page uses a dark theme with indigo/purple accents. To change colors, modify the Tailwind classes:
- Primary: `indigo-500`, `indigo-600`
- Secondary: `purple-500`, `purple-600`
- Accent: `pink-300`

### Calculator Logic
The price calculation is currently using demo values. To integrate with your actual ML model:
1. Replace the `updatePrice()` function in the `<script>` section
2. Make an AJAX call to your `/predict` endpoint
3. Update the display with the real prediction

### Content
Edit the following sections in `landing.html`:
- **Hero Title**: Line 145-150
- **Description**: Line 152-154
- **Features**: Lines 377-417
- **Footer**: Lines 421-435

## Next Steps
1. **Connect to Real API**: Replace demo calculator with actual prediction endpoint
2. **Add More Sections**: Consider adding testimonials, pricing, or FAQ sections
3. **SEO Optimization**: Add meta tags, structured data
4. **Analytics**: Integrate Google Analytics or similar
5. **Performance**: Optimize images and lazy-load components

## Browser Compatibility
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## Notes
- The landing page is standalone and doesn't require React
- All dependencies are loaded via CDN
- No build process required
- Fully customizable with Tailwind classes
