
# Product Image Scraper

This Python script scrapes product images from the Girlfriend Collective website (https://girlfriend.com/) for specified product categories.
## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Scrapes product images from specified categories.
- Downloads images and saves them into structured directories.
- Uses Selenium for handling dynamic content loading.
- Converts product titles to a specific format for file naming.

## Requirements

- Python 3.11
- Google Chrome Browser

## Installation

1. **Clone the repository**:

   \`\`\`
   git clone https://github.com/Hamxay/image-scraper
   \`\`\`

2. **Create a virtual environment** (optional but recommended):

   \`\`\`
   python3 -m venv venv
   source venv/bin/activate   # On Windows use \`venv\Scripts\activate\`
   \`\`\`

3. **Install the required packages**:

   \`\`\`
   pip install -r requirements.txt
   \`\`\`

## Usage

1. **Run the script**:

   \`\`\`
   python scraper.py
   \`\`\`

2. **Configure categories and directories**:
   
   - You can modify the \`base_url\`, \`categories\`, \`image_dir_1\`, and \`image_dir_2\` variables in \`scraper.py\` to customize the scraping targets and image storage paths.

## Project Structure

\`\`\`
product-image-scraper/
│
├── scraper.py               # Main script containing the scraping logic
├── requirements.txt         # Required Python packages
├── README.md                # This README file
├── cloth_images/            # Directory to store clothing images
└── model_images/            # Directory to store model images
\`\`\`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
