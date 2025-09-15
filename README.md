# NUST Society of Artificial Intelligence Website

This project is a one-page website for the NUST Society of Artificial Intelligence, designed to showcase both tech and non-tech portfolios. The website features a modern and responsive design using Bootstrap, with options for dark and light modes.

## Project Structure

```
nsa-website
├── public
│   ├── index.html        # Main HTML document for the website
│   └── favicon.ico       # Favicon for the website
├── src
│   ├── css
│   │   └── styles.css    # Custom CSS styles for the website
│   ├── js
│   │   └── main.js       # JavaScript for interactivity
│   └── assets            # Directory for additional assets (images/icons)
├── package.json          # Configuration file for npm
└── README.md             # Documentation for the project
```

## Features

- Two centered buttons for selecting between Tech and Non-Tech portfolios.
- Further options for "Executive Recruitment" and "Directorate Recruitment."
- Dark and light mode support for enhanced user experience.
- Accessibility features to ensure usability for all users.
- Integration of the Titillium Web font from Google Fonts.
- Responsive design that works on various devices.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd nsa-website
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the project:
   ```
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000` to view the website.

## Deployment

This project is tailored for deployment on Firebase. To deploy:

1. Install Firebase CLI if you haven't already:
   ```
   npm install -g firebase-tools
   ```

2. Login to Firebase:
   ```
   firebase login
   ```

3. Initialize Firebase in your project:
   ```
   firebase init
   ```

4. Deploy the project:
   ```
   firebase deploy
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.