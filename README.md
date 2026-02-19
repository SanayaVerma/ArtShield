# ArtShield
 This simulation is designed for digital artists who want to protect their art from being scraped and reproduced by Generative AI models
 
Demo video: https://www.youtube.com/watch?v=Blq18LMJiAc 

## Problem Statement
Generative AI models are continually scraping the internet, often utilizing the work of digital artists without their permission or compensation. Digital creators need a way to fight back and protect their digital sovereignty. However, true defensive cybersecurity tools require heavy GPU compute and complex machine learning libraries, making it difficult for everyday creators to understand or visualize how their art is actually being protected from AI theft.

## Solution
ArtShield: GenAI Protection Simulator is an interactive educational web app designed to demonstrate the mathematical logic behind real-world AI defense tools. Since running actual adversarial perturbations is computationally heavy, ArtShield simulates two primary defense mechanisms using a proxy of targeted mathematical noise:
1.	Glaze Simulation (Style Masking): Applies high-frequency noise to force a "style drift," tricking an AI vision model into seeing a photograph as a rough charcoal sketch.
2.	Nightshade Simulation (Concept Poisoning): Applies low-frequency noise and OCR data to corrupt the AI's semantic map, forcing it to misinterpret an image entirely (e.g., seeing a city skyline as deep space).
To prove these defenses work, ArtShield integrates directly with the live DALL-E 3 API. By asking the generative AI to reproduce the images, the app visually demonstrates the "cat-and-mouse" game of cybersecurity: the Glazed image forces the AI to generate art in the wrong style, and the Nightshaded image causes a total conceptual collapse, proving that artists can successfully engineer vulnerabilities into AI models to protect their work.

## Links
•	Project URL: https://artshield.streamlit.app/ 

•	GitHub Repository: https://github.com/SanayaVerma/ArtShield 

•	Demo Video: https://youtu.be/Blq18LMJiAc 

## Credits
•	Research Inspiration: The groundbreaking AI cybersecurity research by the SAND Lab at the University of Chicago for pioneering the original [Glaze](https://glaze.cs.uchicago.edu/) and [Nightshade](https://nightshade.cs.uchicago.edu/) tools.

•	Development Assistance: Usage of Gemini for vibe coding and report generation.
