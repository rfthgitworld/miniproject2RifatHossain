# INF601 - Advanced Programming in Python
# Rifat Hossain
# Mini Project 2


# This project will be using Pandas dataframes. This isn't intended to be full blown data science project. The goal here is to come up with some question and then see what API or datasets you can use to get the information needed to answer that question. This will get you familar with working with datasets and asking questions, researching APIs and gathering datasets. If you get stuck here, please email me!
#
# (5/5 points) Initial comments with your name, class and project at the top of your .py file.
# (5/5 points) Proper import of packages used.
# (20/20 points) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
# Think of some question you would like to solve such as:
# "How many homes in the US have access to 100Mbps Internet or more?"
# "How many movies that Ridley Scott directed is on Netflix?" - https://www.kaggle.com/datasets/shivamb/netflix-shows
# Here are some other great datasets: https://www.kaggle.com/datasets
# (10/10 points) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data is labeled tabular data.
# (10/10 points) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build some fancy charts here as it will greatly help you in future homework assignments and in the final project.
# (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the project should save these when it executes. You may want to add this folder to your .gitignore file.
# (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
# (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
# (20/20 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the explanations.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Create charts dir to place the graph plots
Path(r'charts').mkdir(exist_ok=True)

# Load the dataset
df = pd.read_csv('data/health_fitness_tracking_365days.csv')

font1 = {'family':'serif','color':'blue','size':12}
font2 = {'family':'serif','color':'darkred','size':10}


# Sort values so the line plot makes sense
df_sorted = df.sort_values("exercise_minutes")

# 1. Scatter plot to show relationship between exercise minutes and calories burned
plt.figure(figsize=(8, 6))
plt.scatter(df_sorted["exercise_minutes"], df_sorted["calories_burned"])
plt.xlabel('Exercise Minutes', fontdict = font2)
plt.ylabel('Calories Burned', fontdict = font2)
plt.title("Relationship: Exercise Minutes vs Calories Burned", fontdict = font1)
plt.savefig('charts/scatter_exercise_calories.png')

# 2. Do men vs women differ in exercise minutes or calories burned?

gender_group = df.groupby("gender")[["exercise_minutes", "calories_burned"]].mean()

x = np.arange(len(gender_group))  # gender positions
width = 0.35


fig, ax = plt.subplots()
ax.bar(x - width/2, gender_group["exercise_minutes"], width, label="Exercise Minutes")
ax.bar(x + width/2, gender_group["calories_burned"], width, label="Calories Burned")

ax.set_xticks(x)
ax.set_xticklabels(gender_group.index)
ax.set_xlabel("Gender", fontdict = font2)
ax.set_ylabel("Average Value", fontdict = font2)
ax.set_title("Gender Differences: Exercise Minutes vs Calories Burned", font1)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig('charts/bar_exercise_cal.png')


# 3. Does more sleep reduce stress level? (Correlation Heatmap)?

numeric_cols = ['steps', 'heart_rate_avg', 'sleep_hours', 'calories_burned', 'exercise_minutes', 'stress_level', 'weight_kg', 'bmi']
corr = df[numeric_cols].corr()

fig, ax = plt.subplots()
cax = ax.matshow(corr, cmap="coolwarm")
fig.colorbar(cax)
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=90)
ax.set_yticklabels(numeric_cols)
ax.set_title("Correlation Heatmap")
plt.savefig('charts/correlation_heatmap.png')

# 4. Relationship: Heart rate vs Exercise minutes (Bubble chart)

fig, ax = plt.subplots()
scatter = ax.scatter(
    df["exercise_minutes"],
    df["heart_rate_avg"],
    s=df["calories_burned"] / 10,   # scale bubble size
    alpha=0.4
)

ax.set_xlabel("Exercise Minutes")
ax.set_ylabel("Average Heart Rate")
ax.set_title("Heart Rate vs Exercise Minutes (Bubble size = Calories Burned)")
plt.savefig('charts/bubble_cart_heart_rate.png')

# 5. Distribution of BMI categories (Pie chart)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

df["bmi_category"] = df["bmi"].apply(bmi_category)
bmi_counts = df["bmi_category"].value_counts()

fig, ax = plt.subplots()
ax.pie(bmi_counts, labels=bmi_counts.index, autopct="%1.1f%%", startangle=90)
ax.set_title("BMI Category Distribution")
plt.savefig('charts/bmi_category_distribution.png')