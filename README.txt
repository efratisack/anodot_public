# ANODOT-YDATA: LLM Agent-Managed Interface for Business Monitoring
# Efrat Isack, Max Sverdlov
# 16.08.2024

This repository contains inspirational code developed as part of the Ydata final industrial project.
in collaboration with Anodot.
The project successfully demonstrates leveraging the power of Large Language Models (LLMs)
to create agents that replace traditional user interfaces with innovative new ones,
 providing a completely different user experience.

# Project Presentation
For a detailed presentation of this project, you can watch the video here:
https://youtu.be/Amu67gqBmxE?si=_j8H_UIQbCRN0vvI

# GitHub link:
https://github.com/efratisack/anodot_public.git

# Prerequisites
To make the code work, you need to configure the following:
1. Set the LANGCHAIN_API_KEY in the globals.py file.
2. Set the apikey in the globals.py file.

# Modes of Operation
This project offers two modes of operation:
1. Interactive App using Streamlit:
   To enable this mode
   - Set interactive_app = True in the globals.py file.
   - From the terminal, run: streamlit run main.py
2. Offline Tests on Queries in CSV File:
   To enable this mode
   - Set interactive_app = False in the globals.py file.
   - Run test.py
   - Check the results in the \synthetic_data directory

# Acknowledgments
Special thanks to our project mentor Tom Haramaty, and our Anodot guides Ira Cohen and Alexander Shereshevsky for their invaluable support and guidance throughout the project.


