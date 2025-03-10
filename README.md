# Automated Proliferation Assessment 

Repo for the backend for European Healthcare Hackathon 2025

## Problem
Automated Proliferation Assessment in Neuroendocrine Tumors
Develop an AI-powered tool to automate the Ki-67 proliferation index assessment from pathology slides, improving diagnostic efficiency and ensuring standardized, accurate results.
Repo for the backend for European Healthcare Hackathon 2025

What is Ki67?
- Ki67 protein is a marker of cell proliferation (growth).
- It can be detected immunohistochemically.
- The percentage of Ki67+ cells determines the proliferative 
activity of the tumor (its growth rate), which is used to 
establish the tumor grade and reflects the aggressiveness of 
its biological behavior.

However...

- Evaluation should be performed digitally.
- However, in practice, it is still mostly assessed by the human 
eye.
- As a result, the estimation of proliferation is imprecise, which 
can have an impact on the patient.
- Developing an AI algorithm capable of determining proliferative 
activity in NETs.

What should the algorithm be able to do?
1) Determine the percentage of Ki67-positive tumor cells in a 
selected region.
2) Allow manual selection of the region of interest (the pathologist 
can mark the tumor area of interest).
3) Assess the intensity of Ki67 positivity (mild, moderate, strong), as 
available studies suggest this may have prognostic significance.
4) Evaluate the distribution of Ki67-positive cells (is the proliferation)

## Solution

Our solution is a a modern web app that uses computer vision models to assess Ki67-positive cells withen an image uploaded by the user. The image is analyzed by our computer vision model to annotate and count the number of cells from the selected region. 

[![Play](https://github.com/Takosaga/EHH-2025/blob/main/play.png)](https://youtu.be/4LtwRDbN2_M)

## 

Frontend is avaliable [here](https://github.com/lukascer/Automated-Proliferation-Assessment)
Includes the images used and data annotated set up to be used to fine tune [YOLOv11](https://docs.ultralytics.com/models/yolo11/) a pretrained CNN model

Along with python files to create API request to call the model and return values of positive and negative cells to front end
