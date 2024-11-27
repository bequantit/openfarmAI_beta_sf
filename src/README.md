# Source Code Documentation

## Overview
This directory contains the source code for a chatbot application built with Streamlit and OpenAI's GPT models. The application is designed to provide information about dermocosmetic products, their usage, benefits, and ingredients.

## Directory Structure

```
src/
├── chatbot.py
├── parameters.py
├── README.md
├── tools.py
└── settings.py
```

## Components

### chatbot.py
Contains the core chatbot functionality including:
- Logging configuration for chat and email systems
- Message handling and display functions
- Chat interface components
- Header setup and configuration

Key functions:
- `setHeader()`: Configures the application header with image and caption
- `addMessage()`: Adds messages to the conversation state
- `printMessage()`: Displays messages in the chat interface
- `printConversation()`: Renders the complete conversation history

### parameters.py
Stores all configuration parameters and constants including:
- Log file paths
- Asset paths (avatars, logos)
- Email configuration
- OpenAI API parameters
- Database configuration
- Chat interface settings
- Color schemes

### tools.py
Provides utility functions for various operations:
- Email handling and sending
- Image processing and encoding
- Text formatting and manipulation
- Database operations
- Message streaming
- Logging utilities

Key functions:
- `sendEmail()`: Handles email dispatch functionality
- `customImage()`: Image resizing and processing
- `streamMarkdown()`: Creates streaming text effect in chat
- `formatLogMessage()`: Formats log messages for better readability
- `retrieveLastMessage()`: Retrieves and processes chat messages

## Dependencies
- `streamlit`: For web interface
- `PIL`: Image processing
- `openai`: AI model integration
- `logging`: Application logging
- `smtplib`: Email functionality
- `base64`: Image encoding
- `datetime`: Time operations
- Other standard Python libraries

## Usage Example